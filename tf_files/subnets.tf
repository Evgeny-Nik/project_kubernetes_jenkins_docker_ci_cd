#Create Subnets
resource "aws_subnet" "Mysubnet01" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true
  tags = {
    "Name" = "MyPublicSubnet01"
  }
}

resource "aws_subnet" "Mysubnet02" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.region}b"
  map_public_ip_on_launch = true
  tags = {
    "Name" = "MyPublicSubnet02"
  }
}

# Associate Subnets with the Route Table
resource "aws_route_table_association" "Mysubnet01_association" {
  route_table_id = aws_route_table.myroutetable.id
  subnet_id      = aws_subnet.Mysubnet01.id
}

resource "aws_route_table_association" "Mysubnet02_association" {
  route_table_id = aws_route_table.myroutetable.id
  subnet_id      = aws_subnet.Mysubnet02.id
}