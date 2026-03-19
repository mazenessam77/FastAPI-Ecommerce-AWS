###############################################################################
# S3 — Static Assets Bucket (Product Images)
# CloudFront disabled — account requires verification.
# Access S3 directly or re-enable CloudFront once account is verified.
###############################################################################

resource "aws_s3_bucket" "static_assets" {
  bucket = "${var.project_name}-static-assets-${data.aws_caller_identity.current.account_id}"

  tags = { Name = "${var.project_name}-static-assets" }
}

resource "aws_s3_bucket_public_access_block" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_versioning" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_policy" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  depends_on = [aws_s3_bucket_public_access_block.static_assets]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.static_assets.arn}/*"
      }
    ]
  })
}
