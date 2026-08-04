variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

variable "appid" {
  description = "eBay developer appid"
  type        = string
}

variable "devid" {
  description = "eBay developer devid"
  type        = string
}

variable "certid" {
  description = "eBay developer certid"
  type        = string
}

variable "token" {
  description = "eBay developer token"
  type        = string
}

variable "inventory_key" {
  description = "Key used to derive inventory"
  type        = string
}

variable "UPSTASH_REDIS_REST_URL" {
  description = "Upstash redis REST url"
  type        = string
}

variable "UPSTASH_REDIS_REST_TOKEN" {
  description = "Upstash redis REST token"
  type        = string
}