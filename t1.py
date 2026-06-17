# -*- coding: utf-8 -*-
print("سلام دنیا")
num=[5,2,3,5,6]
sum=0
for i in num:
    sum+=i
print("sum=",sum)
l=[11,2,4,6,25,2,44,1,6]
max=l[0]
c=1
while c<len(l):
    if l[c]>max:
        max=l[c]
    c+=1
print("max=",max)
n=[5,17,4,45,6,3]
m1=n[0]
m2=n[1]
for i in n:
    if  i>m1 and i>m2:
        m1=i
    elif i>m2 :
        m2=i

print("max1=",m1)
print("max2=",m2)
ls=[1,1,1,3,3,5,5,5,6,6,6,7,8,8,9,9]
print(ls[0],end=" ")
for i in range(1,len(ls)):
    if ls[i]!=ls[i-1]:
        print(ls[i],end=" ")

ls2=[2,2,2,4,4,5,7,7,7,9,9,11]
c=1
for i in range(1,len(ls2)):
    if ls2[i]== ls2[i-1]:
        c+=1
    else:
        print(ls2[i-1],"=",c)
        c=1
print(ls2[-1],"= ",c)

words = ["ali", "ila", "lia", "eta", "ate", "mrg", "grnm"]
anagrams = {}

for word in words:
    # حروف کلمه را مرتب کرده و به هم می‌چسبانیم
    sorted_word = "".join(sorted(word))

    # اگر این حروف مرتب شده قبلاً در دیکشنری وجود داشت، کلمه را به لیست آن اضافه می‌کنیم
    if sorted_word in anagrams:
        anagrams[sorted_word].append(word)
    # در غیر این صورت، یک لیست جدید برای این حروف مرتب شده ایجاد می‌کنیم
    else:
        anagrams[sorted_word] = [word]

# تبدیل دیکشنری به لیستی از لیست‌ها (کلمات هم‌گروه)
result = list(anagrams.values())

print(result)
class car:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
    def d_p(self):
        print({self.brand},"ghffgfg",{self.model})
m_car=car("bmw","x666")
m_car.d_p()
class bankacunt:
    def __init__(self,onver,balanc=0):
        self.onver=onver
        self._balanc=balanc
    def depoint(self,amont):
        if amont>0:
            self._balanc+=amont
            print("تومان واریز شد",{amont})
        else:
            print("مبلغ واریزی باید مثبت باشد")
    def bard(self,amont):
        if 0<amont <=self._balanc:
            self._balanc-=amont
            print("مبرداشت از حساب",amont)
        else:
            print("موجودی کافی نیست")
    def mojody(self):
        return "نام صاحب حساب:",{self.onver},"موجودی:",{self._balanc}
my_acc=bankacunt("علی",10000)
print( my_acc.mojody())
my_acc.depoint(100)
print(my_acc.mojody())
my_acc.bard(500)
print(my_acc.mojody())
class savebank(bankacunt):
    def __init__(self,onver,balanc=0,rate=0.20):
        super().__init__(onver,balanc)
        self.rate=rate
    def add_rate(self):
        su=self._balanc*self.rate
        self._balanc+=su
        print("mojode:=",[self._balanc])
my_s=savebank("ali",10000,0.50)
print(my_s.mojody())
my_s.add_rate()
class ch_ac(bankacunt):
    def __init__(self, onver, balanc=0,vam=500):
        super().__init__(onver,balanc)
        self.vam=vam
    def bar(self,amont):
        if amont>0 and (self._balanc-amont)> self.vam:
            self._balanc-=amont
            print("توان برداشت",{self._balanc})
        else:
            print("زیادی برداشت")
mc=ch_ac("ahmad",300)
mc.bar(200)
mc.bar(400)
f=["seb","moz","por","gel"]
for i,e in enumerate(f):
    print("index=",i,"elemant=",e)