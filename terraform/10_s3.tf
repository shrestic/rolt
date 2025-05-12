resource "aws_s3_bucket" "rolt_bucket" {
  bucket        = var.aws_bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "rolt_public_block" {
  bucket = aws_s3_bucket.rolt_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false

  depends_on = [aws_s3_bucket.rolt_bucket]
}

resource "aws_s3_bucket_policy" "allow_public_read" {
  bucket = aws_s3_bucket.rolt_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.rolt_bucket.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.rolt_public_block]
}
