class RomanConverter:
    values=[('M',1000),('CM',900),('D',500),('CD',400),('C',100),('XC',90),('L',50),('XL',40),('X',10),('IX',9),('V',5),('IV',4),('I',1)]
    def to_roman(self,num):
        result=''
        for sym,val in self.values:
            while num>=val:
                result+=sym
                num-=val
        return result
    def from_roman(self,s):
        roman_map={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        total=0
        prev=0
        for ch in reversed(s):
            curr=roman_map[ch]
            if curr<prev:
                total-=curr
n            else:
                total+=curr
            prev=curr
        return total
