from django.shortcuts import render
from ninja import Router
from .models import Gym
from users.global_auth import GlobalAuth
from utils.common_schemas import MessageOut

gym_controller = Router(tags=["gym"])

@gym_controller.get("get_all_tenants", auth=GlobalAuth(), response = {
    200: MessageOut,
    500: MessageOut,
})
def get_all_tenants():
    try: gym = Gym.objects.all()
    except Exception as e: return 500, {"message": f"code: 1, message: {e}"}
    
    return 200, {"message": str(gym)}