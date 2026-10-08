# Infrastructure volontairement mal configuree (lab 4) - ne pas appliquer.
resource "aws_s3_bucket" "receipts" {
  bucket = "sunupay-receipts"
  acl    = "public-read"
}

resource "aws_security_group" "api" {
  name = "sunupay-api"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "ledger" {
  identifier          = "sunupay-ledger"
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  username            = "sunupay"
  password            = var.db_password
  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
}

# Lab 1 corrige : le mot de passe est fourni au moment du deploiement, il n'est plus ecrit ici.
variable "db_password" {
  type      = string
  sensitive = true
}
