from django.db import models
from halls.models import Hall
from users.models import User
from django.core.mail import EmailMessage
# Create your models here.

class Questions(models.Model):
	question = models.TextField(max_length=200)
	answer = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def save(self, **kwargs):
		"""
		Saves the model to the DB.
		Emails the user if answer has been added.
		"""
		super().save(**kwargs)

		if(self.answer != ""):
			mail_subject = "Your Question has been answered."
			# Do not break the following string or the email will get cut off
			message = f"Hi {self.user.first_name},\n\n You're receiving this email because you asked a question about {self.hall.name}. The HonestHalls team has now answered your question! Revisit the {self.hall.name} hall page to see their response.\n\n"

			email = EmailMessage(
				mail_subject, message, to=[self.user.email]
			)
			email.send()

	def delete(self, **kwargs):
		mail_subject = "Your Question has been deleted."
		# Do not break the following string or the email will get cut off
		message = f"Hi {self.user.first_name},\n\n You're receiving this email because you asked a question about {self.hall.name}. The HonestHalls team has reviewed your question and chosen to delete it. This may be down to it be a repeat question or because the team felt it was inappropriate.\n\n"
		email = EmailMessage(
			mail_subject, message, to=[self.user.email]
		)
		email.send()
		super().delete(**kwargs)
