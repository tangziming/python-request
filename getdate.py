import time 







def getdate(day):
    day = int(day)
    now = time.time()
    ago = now - day * 24 * 60 *60 
    date = time.strftime('%Y-%m-%d',time.localtime(ago))
    return date



if __name__=='__main__':
    print(getdate(0))
    print(getdate(10))     



# sql = '''
# select *
#   from (select goodscode, goodsname, sum(realnumber)
#           from (select a.goodscode, c.goodsname, a.realnumber
#                   from t_exterbilldetail a, t_exterbill b, t_goods c
#                  where a.billid = b.billid
#                    and b.billstatus in ('1', '2', '3')
#                    and b.operatetime <= to_date('{today}', 'YYYY-MM-DD')
#                    and b.operatetime >= to_date('{date}', 'YYYY-MM-DD')
#                    and b.billtype = '112'
#                    and a.goodscode = c.goodscode
                
#                 union all
#                 select a.goodscode, c.goodsname, -a.realnumber
#                   from t_exterbilldetail a, t_exterbill b, t_goods c
#                  where a.billid = b.billid
#                    and b.billstatus in ('1', '2', '3')
#                    and b.operatetime <= to_date('{today}', 'YYYY-MM-DD')
#                    and b.operatetime >= to_date('{date}', 'YYYY-MM-DD')
#                    and b.billtype = '113'
#                    and a.goodscode = c.goodscode)
#          group by goodscode, goodsname
#          order by sum(realnumber) desc)
#  where rownum < 3

# '''.format(today=getdate(0),date=getdate(10))


# print(sql)