variable "region" {
  type    = string
  default = "eu-north-1"
}

variable "key_pair_name" {
  description = "key_pair_name"
  type        = string
  default     = "kubernetes_project"
}

variable "instance_type" {
  description = "instance_type"
  type        = string
  default     = "t3.micro"
}

variable "capacity_type" {
  description = "capacity_type"
  type        = string
  default     = "ON_DEMAND"
}

variable "disk_size" {
  description = "disk_size"
  type        = number
  default     = 20
}