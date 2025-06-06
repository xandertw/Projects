check = ""
b=-1
palindrome = input()
palindrome = palindrome.replace(',', '')
palindrome = palindrome.replace('.', '')
palindrome = palindrome.lower()
palindrome = palindrome.replace(" ","")
for letter in palindrome:
    b=b+1
while (b>-1):
    check +=  palindrome[b]
    b=b-1
print(check)
print(palindrome)
if (check == palindrome):
    print("true")
else:
    print("false")