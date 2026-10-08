# Infrastructure corrigee (lab 4) - ne pas appliquer.

variable "db_password" {
  type      = string
  sensitive = true
}

variable "admin_cidr" {
  type        = string
  description = "Plage d'adresses du reseau interne SunuPay"
  default     = "10.0.0.0/16"
}

resource "aws_kms_key" "sunupay" {
  description         = "Cle de chiffrement SunuPay"
  enable_key_rotation = true
}

# Le stockage des recus n'est plus public et il est chiffre
resource "aws_s3_bucket" "receipts" {
  bucket = "sunupay-receipts"
}

resource "aws_s3_bucket_public_access_block" "receipts" {
  bucket                  = aws_s3_bucket.receipts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "receipts" {
  bucket = aws_s3_bucket.receipts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.sunupay.arn
    }
  }
}

resource "aws_s3_bucket_versioning" "receipts" {
  bucket = aws_s3_bucket.receipts.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Les acces ne sont plus ouverts a tout Internet
resource "aws_security_group" "api" {
  name        = "sunupay-api"
  description = "Acces a l'API SunuPay depuis le reseau interne uniquement"

  ingress {
    description = "API depuis le reseau interne"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }
}

# La base n'est plus accessible depuis Internet, elle est chiffree,
# et son mot de passe n'est plus ecrit dans le fichier
resource "aws_db_instance" "ledger" {
  identifier                          = "sunupay-ledger"
  engine                              = "postgres"
  instance_class                      = "db.t3.micro"
  allocated_storage                   = 20
  username                            = "sunupay"
  password                            = var.db_password
  publicly_accessible                 = false
  storage_encrypted                   = true
  kms_key_id                          = aws_kms_key.sunupay.arn
  backup_retention_period             = 7
  deletion_protection                 = true
  iam_database_authentication_enabled = true
  performance_insights_enabled        = true
  performance_insights_kms_key_id     = aws_kms_key.sunupay.arn
  skip_final_snapshot                 = false
  final_snapshot_identifier           = "sunupay-ledger-final"
}
