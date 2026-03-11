-----<
x = 0
y := 3x - 1
x
while x < 10 {
    y
    x = x + 1
}
x

for i in 1..x {
    x = x - 1
    x
}
----->

-----<
dist X (Norm 3 2)
dist Y (Die 5)
z = E(X + Y) 
z
dist X (PMF [0 0.5] [1 0.5])
----->

-----< 
func woof (x y) {
    z = x + y
    return z
}

woof (5 4)
----->

-----<
When you import a library, you essentially add new keywords into the program, and therefore it is important that libraries do not have any conflicting keywords - theres not enough libraries to justify using the bullet point tbh....
----->

