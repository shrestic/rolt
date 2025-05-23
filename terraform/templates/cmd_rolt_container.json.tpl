[
  {
    "name": "rolt-cmd-exe",
    "image": "${docker_image_url_django}",
    "essential": true,
    "cpu": 10,
    "memory": 512,
    "command": ["/bin/sh", "-c", "${command}"],
    "environment": [
      { "name": "ALLOWED_HOSTS", "value": "${allowed_hosts}" },
      { "name": "ADMIN_USERNAME", "value": "${admin_username}" },
      { "name": "ADMIN_PASSWORD", "value": "${admin_password}" },
      { "name": "ADMIN_EMAIL", "value": "${admin_email}" },
      { "name": "DEFAULT_FROM_EMAIL", "value": "${default_from_email}" },
      { "name": "DJANGO_ADMIN_URL", "value": "${admin_url}" },
      { "name": "DJANGO_AWS_ACCESS_KEY_ID", "value": "${aws_access_key_id}" },
      { "name": "DJANGO_AWS_S3_CUSTOM_DOMAIN", "value": "${aws_s3_custom_domain}" },
      { "name": "DJANGO_AWS_S3_MAX_MEMORY_SIZE", "value": "100000000" },
      { "name": "DJANGO_AWS_S3_REGION_NAME", "value": "${region}" },
      { "name": "DJANGO_AWS_SECRET_ACCESS_KEY", "value": "${aws_secret_access_key}" },
      { "name": "DJANGO_AWS_STORAGE_BUCKET_NAME", "value": "${aws_bucket_name}" },
      { "name": "DJANGO_DEBUG", "value": "${django_debug}" },
      { "name": "DJANGO_EMAIL_BACKEND", "value": "django.core.mail.backends.smtp.EmailBackend" },
      { "name": "DJANGO_EMAIL_SUBJECT_PREFIX", "value": "[rolt]" },
      { "name": "DJANGO_SECRET_KEY", "value": "${django_secret_key}" },
      { "name": "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", "value": "True" },
      { "name": "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "value": "True" },
      { "name": "DJANGO_SECURE_HSTS_PRELOAD", "value": "True" },
      { "name": "DJANGO_SECURE_HSTS_SECONDS", "value": "518400" },
      { "name": "DJANGO_SECURE_SSL_REDIRECT", "value": "True" },
      { "name": "DJANGO_SERVER_EMAIL", "value": "${server_email}" },
      { "name": "DJANGO_SETTINGS_MODULE", "value": "${django_settings_module}" },
      { "name": "DOMAIN", "value": "www.rolt.cloud" },
      { "name": "EMAIL_HOST", "value": "smtp.sendgrid.net" },
      { "name": "EMAIL_HOST_PASSWORD", "value": "${sendgrid_api_key}" },
      { "name": "EMAIL_HOST_USER", "value": "apikey" },
      { "name": "EMAIL_PORT", "value": "587" },
      { "name": "EMAIL_USE_TLS", "value": "True" },
      { "name": "POSTGRES_DB", "value": "${db_name}" },
      { "name": "POSTGRES_HOST", "value": "${db_host}" },
      { "name": "POSTGRES_PASSWORD", "value": "${db_password}" },
      { "name": "POSTGRES_PORT", "value": "${db_port}" },
      { "name": "POSTGRES_USER", "value": "${db_user}" },
      { "name": "REDIS_URL", "value": "${redis_url}" },
      { "name": "SITE_NAME", "value": "Rolt" },
      { "name": "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "value": "${google_oauth2_key}" },
      { "name": "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "value": "${google_oauth2_secret}" },
      { "name": "SUPPORT_ALERT_EMAIL", "value": "${support_alert_email}" },
      { "name": "TEMP_DOMAIN", "value": "${temp_domain}" },
      { "name": "VNPAY_API_URL", "value": "https://sandbox.vnpayment.vn/merchant_webapi/api/transaction" },
      { "name": "VNPAY_HASH_SECRET_KEY", "value": "${vnpay_hash_secret_key}" },
      { "name": "VNPAY_PAYMENT_URL", "value": "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html" },
      { "name": "VNPAY_RETURN_URL", "value": "${vnpay_return_url}" },
      { "name": "VNPAY_TMN_CODE", "value": "${vnpay_tmn_code}" }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/rolt-cmd-exe",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "rolt-cmd-exe-log-stream"
      }
    }
  }
]
