# this file helps to predict everyday movement top or bottom.
a=[2,1,3,2,5,1]
b=[3,2,3,4,5,1]

# for j in range(1,len(a)):
#     for i in range(0,len(a)-j):
#         if a[i] > a[i+1]:
#             a[i], a[i+1] = a[i+1], a[i]
# print(a)

def bubble_sorted(iterable):
    new_list = list(iterable)
    list_len = len(new_list)
    for i in range(list_len):
        for j in range(i + 1,list_len):
            if new_list[i] > new_list[j]:
                new_list[i], new_list[j] = new_list[j], new_list[i]
    return new_list

print(bubble_sorted(a))
