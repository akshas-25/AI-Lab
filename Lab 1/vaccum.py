clean=0
dirt=1
for i in range(0,4):
    curr=int(input(f"room {i+1} clean/dirty(0/1):"))
    if curr==dirt :
     print(f"Cleaned room {i+1}")
    else :
     print(f"room {i+1} is already clean moving to the next")
     