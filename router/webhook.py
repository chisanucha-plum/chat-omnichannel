from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
import logging

from service.rocket import RocketChatClient
from model.user import Visitor
from service.line import LineService

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/healthcheck")
async def healthcheck():
    return "OK"

@router.post("/line", status_code=status.HTTP_200_OK)
async def line_webhook(request: Request, response: Response):
    try:
        body = await request.json()
        logger.info(f"Received LINE webhook body: {body}")
        
        events = body.get("events", [])
        logger.info(f"Found {len(events)} events")
        
        # สร้าง instance ของ LineService
        oa_uid = body.get("destination")  # รับ channel_access_token จาก bodทนที่ด้วย token ของคุณ
        line_service = LineService(oa_uid)
        
        for event in events:
            logger.info(f"Processing event: {event}")
            if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
                user_text = event["message"]["text"]
                user_id = event["source"]["userId"]
                
                logger.info(f"Received text from LINE user {user_id}: {user_text}")

                # ดึงข้อมูลโปรไฟล์ของผู้ใช้
                profile_data = line_service.get_user_profile(user_id)
                if profile_data:
                    user_name = f"[LINE] {profile_data.get('displayName', 'Unknown')}"
                    user_picture = profile_data.get("pictureUrl", "")
                    logger.info(f"User name: {user_name}, Picture URL: {user_picture}")
                else:
                    logger.error("Failed to retrieve user profile")
                    user_name = f"LINE User ({user_id})"
                    user_picture = ""

                # ใช้ Line User ID เป็น visitor token
                visitor_token = user_id
                logger.info(f"Using LINE user ID as visitor token: {visitor_token}")

                # สร้าง visitor object
                visitor = Visitor(
                    token=visitor_token,  
                    username=f"line_{visitor_token}",  
                    name=user_name,              
                    department="[LINE]สอบถามเพิ่มเติม"
                )

        
                client = RocketChatClient()
            
                logger.info(f"Creating/Updating visitor with token: {visitor_token}")
                visitor_response = client.create_livechat_visitor(visitor)
                if not visitor_response.get("success"):
                    logger.error(f"Failed to create visitor: {visitor_response}")
                    raise Exception("Failed to create visitor")
                logger.info(f"Visitor created/updated successfully: {visitor_response}")

                
                logger.info(f"Getting/Creating room for visitor token: {visitor_token}")
                room_response = client.get_livechat_room(token=visitor_token)
                if not room_response.get("success"):
                    logger.error(f"Failed to get/create room: {room_response}")
                    raise Exception("Failed to get/create room")

                room = room_response.get("room")
                if not room:
                    logger.error("Room not found in response")
                    raise Exception("Room not found in response")

                room_id = room.get("_id")
                if not room_id:
                    logger.error("Room ID not found")
                    raise Exception("Room ID not found")
                logger.info(f"Using room ID: {room_id}")


                # ส่งข้อความเข้า Rocket.Chat LiveChat
                logger.info(f"Sending message to room {room_id}")
                rocket_response = client.send_livechat_message(
                    token=visitor_token,
                    rid=room_id,
                    msg=user_text
                )

                if not rocket_response.get("success"):
                    logger.error(f"Failed to send message: {rocket_response}")
                    raise Exception("Failed to send message")

                logger.info(f"Message sent successfully: {rocket_response}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "error", "detail": str(e)}
        )

@router.post("/rocket", status_code=status.HTTP_200_OK)
async def rocket_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Received Rocket.Chat webhook: {body}")

        
        messages = body.get("messages", [])
        if not messages:
            return JSONResponse(content={"status": "no message"}, status_code=200)

        message = messages[0]
        msg_text = message.get("msg")
        visitor_token = body.get("visitor", {}).get("token")

        
        line_user_id = visitor_token

        
        channel_access_token = body.get("channel", {}).get("channel_access_token")
        line_service = LineService(channel_access_token)
        send_result = line_service.send_text_message(user_id=line_user_id, text=msg_text)

        logger.info(f"Sent LINE message result: {send_result}")

        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        logger.error(f"Error processing Rocket.Chat webhook: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "detail": str(e)}
        )
