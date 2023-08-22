variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "Cluster_name" {
  description = "Cluster Name"
  type = string
  default = "sample"
}

variable "VPC_name" {
  description = "VPC Name"
  type = string
  default = "VPC_sample"
  
}
variable "Bucket_name" {
  description = "Bucket Name"
  type = string
  default = "hemnettask"
  
}