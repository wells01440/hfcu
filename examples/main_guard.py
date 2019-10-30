def bar():
    print("Hey look! I'm inside the bar")


print("before __name__ guard.  I get run every time my module is used")

if __name__ == "__main__":
    bar()

print("after__name__ guard.  I also get run every time")
