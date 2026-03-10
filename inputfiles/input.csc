-----< 
open comments
x = 5
y (x) := 2*x
for i in 1..x {
    out i
}
close comments
-----> 

var y = 1
out y

-----<
var y = 28932
y 
b = 3
c = 4
a (b c) := 3*b + 4*c
out a
-----> 

y = 1
y

z (x) := 4*x - 1
for x in 1..60 {
    z
}


cost = 1
tax = 1
price (cost tax) := 5*cost
while price < 50 {
    cost = cost + 1
}
cost
price
tax