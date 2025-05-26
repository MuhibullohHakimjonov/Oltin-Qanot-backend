import random
from django.core.cache import cache
from eskiz_sms import EskizSMS

from config.settings import ESKIZ_EMAIL, ESKIZ_PASSWORD
from .models import PhoneVerification


def generate_sms_code():
	return ''.join(random.choices('0123456789', k=6))


def send_verification_sms(phone_number):
	code = generate_sms_code()
	eskiz = EskizSMS(
		email=ESKIZ_EMAIL,
		password=ESKIZ_PASSWORD
	)
	formatted_phone = phone_number.replace('+', '')

	message = f"Oltin Qanot websaytiga kirish uchun tastiqlash kodingiz: {code}"

	try:
		eskiz.send_sms(
			mobile_phone=formatted_phone,
			message=message,
			from_whom='4546'
		)
		PhoneVerification.objects.update_or_create(
			phone_number=formatted_phone,
			defaults={'code': code, 'is_verified': False}
		)
		cache.set(f"sms_code_{formatted_phone}", code, timeout=300)  # код хранится 5 минут
		return True
	except Exception as e:
		print("SMS sending failed:", e)
		return False


def verify_code(phone_number, code):
	formatted_phone = phone_number.replace('+', '')
	cached_code = cache.get(f"sms_code_{formatted_phone}")
	if cached_code == code:
		try:
			verification = PhoneVerification.objects.get(phone_number=formatted_phone, code=code)
			verification.is_verified = True
			verification.save()
			cache.delete(f"sms_code_{formatted_phone}")  # Удаляем код из кеша после успешной проверки
			return True
		except PhoneVerification.DoesNotExist:
			return False
	return False
