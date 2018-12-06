import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import csv

#写入csv文件头部
def save_to_csv():
    with open('data2.csv', 'a', newline='') as csvfile:
        fieldnames = ['date', 'deviceModel', 'provider', 'condition', 'networks', 'quote']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.close()

#获取页面源码
def get_html(url):
    #url = url.format(product_name)
    header = {
        'cookie': '__cfduid=de7deb1e61d98f9d432de467cd77e98441543490108; musicMagpieTn=5FE1F0B7683BBAC54C2D032107835A2F6BDB0E83A6DF111A47ABC493EE9061AE888A1FA6F263EDEA95EC3D495431DDDA34B200FE9290982E012E774F4B6CBC07BD9C1287FC18D7D85096786301376ECB784DA9A4ABD925150410F38E3858CAA77CEBE6B336C0C69E3A834AAB7D1C6A47FDBCB46BD444AE04C081CB451951A02DE330AD6F02DECAFA55B3EBF52F99109F2AEB962F9AA4041B34299107EA93FED7CB4CCA9755F7203DCDE9A61700AFE05068C35AC3; _gcl_au=1.1.940839126.1543490112; _vwo_uuid_v2=D0F013B58C86101460B636FF2677E7BAF|5156c9d6d1a1c2133aefd558084a02af; _vwo_uuid=D0F013B58C86101460B636FF2677E7BAF; _vis_opt_exp_125_combi=2; cto_lwid=b67ea5cf-9049-4186-a71f-c585603c81fc; _ga=GA1.3.1530726585.1543490119; _gid=GA1.3.611423417.1543490119; __utmz=169673277.1543490119.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __qca=P0-141830454-1543490140981; _hjDonePolls=366589; _vis_opt_exp_125_goal_1=1; _hjMinimizedPolls=366589; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; __utma=169673277.1530726585.1543490119.1543498372.1543558286.4; __utmc=169673277; __utmb=169673277.1.10.1543558286; _hjIncludedInSample=1; musicMagpieVal=barcode=i000000007160&networkBarcode=i000000007169&condition=5&aff=1; MMLastTech=parentCode=i000000007160&networkBarcode=i000000007169&condition=5&dateCreated=11/30/2018 6:21:54 AM&dateLastPoppedUp=11/30/2018 6:21:54 AM; _gat_UA-67691761-1=1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    try:
        web_data = requests.get(url,headers=header).text
        return web_data
    except :
        print('Connection Error...')


#通过url和表单参数来以post方式提交获取数据
def get_data(url,EVENTTARGET,num):
    header = {
        'cookie': '__cfduid=de7deb1e61d98f9d432de467cd77e98441543490108; musicMagpieTn=5FE1F0B7683BBAC54C2D032107835A2F6BDB0E83A6DF111A47ABC493EE9061AE888A1FA6F263EDEA95EC3D495431DDDA34B200FE9290982E012E774F4B6CBC07BD9C1287FC18D7D85096786301376ECB784DA9A4ABD925150410F38E3858CAA77CEBE6B336C0C69E3A834AAB7D1C6A47FDBCB46BD444AE04C081CB451951A02DE330AD6F02DECAFA55B3EBF52F99109F2AEB962F9AA4041B34299107EA93FED7CB4CCA9755F7203DCDE9A61700AFE05068C35AC3; _gcl_au=1.1.940839126.1543490112; _vwo_uuid_v2=D0F013B58C86101460B636FF2677E7BAF|5156c9d6d1a1c2133aefd558084a02af; _vwo_uuid=D0F013B58C86101460B636FF2677E7BAF; _vis_opt_exp_125_combi=2; cto_lwid=b67ea5cf-9049-4186-a71f-c585603c81fc; _ga=GA1.3.1530726585.1543490119; _gid=GA1.3.611423417.1543490119; __utmz=169673277.1543490119.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __qca=P0-141830454-1543490140981; _hjDonePolls=366589; _vis_opt_exp_125_goal_1=1; _hjMinimizedPolls=366589; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; __utma=169673277.1530726585.1543490119.1543498372.1543558286.4; __utmc=169673277; _hjIncludedInSample=1; __utmb=169673277.7.10.1543558286; musicMagpieVal=barcode=i000000007160&networkBarcode=i000000007162&condition=5&aff=1; MMLastTech=parentCode=i000000007160&networkBarcode=i000000007162&condition=5&dateCreated=11/30/2018 7:23:16 AM&dateLastPoppedUp=11/30/2018 7:23:16 AM; _gat_UA-67691761-1=1',
        'origin': 'https://www.musicmagpie.co.uk',
        'referer': 'https://www.musicmagpie.co.uk/start-selling/basket-condition-alt?barcode=i000000007160',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    post_data = {
        'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$networkScriptManager': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$UpdatePanel1|ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$RptNetwork$ctl01$NetworkBtn',
        'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$signIn_8$hdn_BasketValue': '0',
        'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$ddlNetwork': num,
        '__EVENTTARGET': EVENTTARGET,
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwUENTM4MQ9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCAgIPZBYCZg9kFgJmDxYCHgRUZXh0Ba4BPHNjcmlwdD4gd2luZG93LmRhdGFMYXllciA9IHdpbmRvdy5kYXRhTGF5ZXIgfHwgW107IHdpbmRvdy5kYXRhTGF5ZXIucHVzaCh7ImxvZ2dlZEluIiA6ICJGYWxzZSIsICJwYWdlVHlwZSIgOiAiYmFza2V0IHBhZ2UiLCAicGFnZUNhdGVnb3J5IiA6ICJ0ZWNoIGNvbmRpdGlvbnMiICx9KTsgPC9zY3JpcHQ+ZAIBEGRkFgRmD2QWAmYPZBYCAgYPFgIeB1Zpc2libGVoZAIGD2QWAgIDD2QWAmYPDxYYHgtUZWNoSGFzTmV0cwIKHg9Qcm9kdWN0SW5mb1NpemUyzAMAAQAAAP////8BAAAAAAAAAAwCAAAAUXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLCBWZXJzaW9uPTEuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAwDAAAASVN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkFAQAAAEJ1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucy5zZXJ2aWNlVmFsdWF0aW9uLkVsZWN0cm9uaWNzUHJvZHVjdEluZm8FAAAACGltZ0ZpZWxkCW1ha2VGaWVsZAptb2RlbEZpZWxkCXR5cGVGaWVsZBRQcm9wZXJ0eUNoYW5nZWRFdmVudAEBAQEEMVN5c3RlbS5Db21wb25lbnRNb2RlbC5Qcm9wZXJ0eUNoYW5nZWRFdmVudEhhbmRsZXIDAAAAAgAAAAYEAAAAEmlwaG9uZS9pcGhvbmU3LmpwZwYFAAAABUFwcGxlBgYAAAAPaVBob25lIDcgKDMyZ2IpBgcAAAANTW9iaWxlIHBob25lcwoLHgpFbGVjUHJpY2VzMqcFAAEAAAD/////AQAAAAAAAAAMAgAAAFF1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucywgVmVyc2lvbj0xLjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAADx1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucy5zZXJ2aWNlVmFsdWF0aW9uLkVsZWN0cm9uaWNQcmljZXMDAAAADUxpc3RgMStfaXRlbXMMTGlzdGAxK19zaXplD0xpc3RgMStfdmVyc2lvbgQAAD11bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucy5zZXJ2aWNlVmFsdWF0aW9uLkVsZWN0cm9uaWNQcmljZVtdAgAAAAgIAgAAAAkDAAAAAQAAAAEAAAAHAwAAAAABAAAABAAAAAQ7dW1icmFjb0NvbnRyb2xzX1ZhbHVhdGlvbnMuc2VydmljZVZhbHVhdGlvbi5FbGVjdHJvbmljUHJpY2UCAAAACQQAAAANAwwFAAAASVN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkFBAAAADt1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucy5zZXJ2aWNlVmFsdWF0aW9uLkVsZWN0cm9uaWNQcmljZQQAAAALZmF1bHR5RmllbGQJZ29vZEZpZWxkCXBvb3JGaWVsZBRQcm9wZXJ0eUNoYW5nZWRFdmVudAAAAAQFBQUxU3lzdGVtLkNvbXBvbmVudE1vZGVsLlByb3BlcnR5Q2hhbmdlZEV2ZW50SGFuZGxlcgUAAAACAAAABTY0LjUwBjIxNS4wMAYxMjkuMDAKCx4LTW9iTmV0d29ya3MynQcAAQAAAP////8BAAAAAAAAAAwCAAAAUXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLCBWZXJzaW9uPTEuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAOnVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLnNlcnZpY2VWYWx1YXRpb24uTW9iaWxlTmV0d29ya3MDAAAADUxpc3RgMStfaXRlbXMMTGlzdGAxK19zaXplD0xpc3RgMStfdmVyc2lvbgQAADt1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucy5zZXJ2aWNlVmFsdWF0aW9uLk1vYmlsZU5ldHdvcmtbXQIAAAAICAIAAAAJAwAAAAoAAAAKAAAABwMAAAAAAQAAABAAAAAEOXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLnNlcnZpY2VWYWx1YXRpb24uTW9iaWxlTmV0d29yawIAAAAJBAAAAAkFAAAACQYAAAAJBwAAAAkIAAAACQkAAAAJCgAAAAkLAAAACQwAAAAJDQAAAA0GDA4AAABJU3lzdGVtLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OQUEAAAAOXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLnNlcnZpY2VWYWx1YXRpb24uTW9iaWxlTmV0d29yawMAAAAHaWRGaWVsZAxuZXR3b3JrRmllbGQUUHJvcGVydHlDaGFuZ2VkRXZlbnQAAQQIMVN5c3RlbS5Db21wb25lbnRNb2RlbC5Qcm9wZXJ0eUNoYW5nZWRFdmVudEhhbmRsZXIOAAAAAgAAAAAAAAAGDwAAAAhVbmxvY2tlZAoBBQAAAAQAAAAIAAAABhAAAAACTzIKAQYAAAAEAAAAAgAAAAYRAAAAAkVFCgEHAAAABAAAAAUAAAAGEgAAAAhWb2RhZm9uZQoBCAAAAAQAAAABAAAABhMAAAAGT3JhbmdlCgEJAAAABAAAAAMAAAAGFAAAAAhULU1vYmlsZQoBCgAAAAQAAAAGAAAABhUAAAABMwoBCwAAAAQAAAAEAAAABhYAAAAGVmlyZ2luCgEMAAAABAAAAAcAAAAGFwAAAAVUZXNjbwoBDQAAAAQAAAAJAAAABhgAAAAHVW5rbm93bgoLHg9Db25kaXRpb25zVGV4dHMy6A4AAQAAAP////8BAAAAAAAAAAwCAAAAUXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLCBWZXJzaW9uPTEuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAPnVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLnNlcnZpY2VWYWx1YXRpb24uVGVjaENvbmRpdGlvblRleHRzAwAAAA1MaXN0YDErX2l0ZW1zDExpc3RgMStfc2l6ZQ9MaXN0YDErX3ZlcnNpb24EAAA/dW1icmFjb0NvbnRyb2xzX1ZhbHVhdGlvbnMuc2VydmljZVZhbHVhdGlvbi5UZWNoQ29uZGl0aW9uVGV4dFtdAgAAAAgIAgAAAAkDAAAADwAAAA8AAAAHAwAAAAABAAAAEAAAAAQ9dW1icmFjb0NvbnRyb2xzX1ZhbHVhdGlvbnMuc2VydmljZVZhbHVhdGlvbi5UZWNoQ29uZGl0aW9uVGV4dAIAAAAJBAAAAAkFAAAACQYAAAAJBwAAAAkIAAAACQkAAAAJCgAAAAkLAAAACQwAAAAJDQAAAAkOAAAACQ8AAAAJEAAAAAkRAAAACRIAAAAKDBMAAABJU3lzdGVtLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OQUEAAAAPXVtYnJhY29Db250cm9sc19WYWx1YXRpb25zLnNlcnZpY2VWYWx1YXRpb24uVGVjaENvbmRpdGlvblRleHQFAAAACWNvbmRGaWVsZBBkZXNjcmlwdGlvbkZpZWxkDXNlcXVlbmNlRmllbGQRdGVjaF90eXBlX2lkRmllbGQUUHJvcGVydHlDaGFuZ2VkRXZlbnQAAQAABAgICDFTeXN0ZW0uQ29tcG9uZW50TW9kZWwuUHJvcGVydHlDaGFuZ2VkRXZlbnRIYW5kbGVyEwAAAAIAAAAFAAAABhQAAABHWW91IGRvbuKAmXQgbmVlZCB0byBzZW5kIHlvdXIgY2hhcmdlciwgYWNjZXNzb3JpZXMgb3IgdGhlIG9yaWdpbmFsIGJveCEAAAAADwAAAAoBBQAAAAQAAAAFAAAABhUAAAAdRXZlcnl0aGluZyB3b3JrcyBhcyBpdCBzaG91bGQBAAAADwAAAAoBBgAAAAQAAAAFAAAABhYAAAA8Tm8gbWFqb3IgZGFtYWdlIChpLmUgY2hpcHMgb3IgY3JhY2tzIHRvIHRoZSBzY3JlZW4gb3IgcGhvbmUpAgAAAA8AAAAKAQcAAAAEAAAABQAAAAYXAAAAD05vIHdhdGVyIGRhbWFnZQMAAAAPAAAACgEIAAAABAAAAAUAAAAGGAAAAB5MaWdodCB3ZWFyIGFuZCB0ZWFyIGFjY2VwdGFibGUEAAAADwAAAAoBCQAAAAQAAAAGAAAABhkAAABHWW91IGRvbuKAmXQgbmVlZCB0byBzZW5kIHlvdXIgY2hhcmdlciwgYWNjZXNzb3JpZXMgb3IgdGhlIG9yaWdpbmFsIGJveCEAAAAADwAAAAoBCgAAAAQAAAAGAAAABhoAAAAdRXZlcnl0aGluZyB3b3JrcyBhcyBpdCBzaG91bGQBAAAADwAAAAoBCwAAAAQAAAAGAAAABhsAAAA9SGVhdnkgd2VhciBhbmQgdGVhciwgc3VjaCBhcyBzY3VmZnMsIGRlbnRzIGFuZCBkZWVwIHNjcmF0Y2hlcwIAAAAPAAAACgEMAAAABAAAAAYAAAAGHAAAAAEgYwAAAA8AAAAKAQ0AAAAEAAAABwAAAAYdAAAAR1lvdSBkb27igJl0IG5lZWQgdG8gc2VuZCB5b3VyIGNoYXJnZXIsIGFjY2Vzc29yaWVzIG9yIHRoZSBvcmlnaW5hbCBib3ghAAAAAA8AAAAKAQ4AAAAEAAAABwAAAAYeAAAASU1ham9yIHNvZnR3YXJlL2hhcmR3YXJlIGlzc3VlcyAoaS5lLiB0aGUgcGhvbmUgZnJlZXplcy9jcmFzaGVzIHJlZ3VsYXJseSkBAAAADwAAAAoBDwAAAAQAAAAHAAAABh8AAAAbU2lnbmlmaWNhbnQgcGh5c2ljYWwgZGFtYWdlAgAAAA8AAAAKARAAAAAEAAAABwAAAAYgAAAAQ0ZhdWx0eSBzY3JlZW4gKGluY2x1ZGluZyBjcmFja3MsIGRpc2NvbG91cmF0aW9uIGFuZCBkYW1hZ2VkIHBpeGVscykDAAAADwAAAAoBEQAAAAQAAAAHAAAABiEAAAAMV2F0ZXIgZGFtYWdlBAAAAA8AAAAKARIAAAAEAAAABwAAAAYiAAAAaVBsZWFzZSBub3RlOiB3ZSBjYW5ub3QgYnV5IHlvdXIgcGhvbmUgaWYgaXQgaXMgbWlzc2luZyBjb21wb25lbnRzIG9yIGlzIGJlbnQsIGNyYXNoZWQgb3Igc25hcHBlZCBpbiBoYWxmLgUAAAAPAAAACgseCXN0ckJhbm5lcgUFQVBQTEUeDUJvb2xBZmZpbGlhdGVnHgpzdHJCYXJjb2RlBQ1pMDAwMDAwMDA3MTYwHhFzdHJOZXR3b3JrQmFyY29kZQUNaTAwMDAwMDAwNzE2OB4SUHJvZHVjdEluZm9TaXplMzAwMvoDAAEAAAD/////AQAAAAAAAAAMAgAAAFF1bWJyYWNvQ29udHJvbHNfVmFsdWF0aW9ucywgVmVyc2lvbj0xLjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwMAwAAAElTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5BQEAAABLdW1icmFjb0NvbnRyb2xzX1ZhbHVhdGlvbnMuc2VydmljZVZhbHVhdGlvbi5FbGVjdHJvbmljc1Byb2R1Y3RJbmZvU2l6ZTMwMF8yBgAAAAxpbWdfMzAwRmllbGQJbWFrZUZpZWxkCm1vZGVsRmllbGQJc2l6ZUZpZWxkCXR5cGVGaWVsZBRQcm9wZXJ0eUNoYW5nZWRFdmVudAEBAQEBBDFTeXN0ZW0uQ29tcG9uZW50TW9kZWwuUHJvcGVydHlDaGFuZ2VkRXZlbnRIYW5kbGVyAwAAAAIAAAAGBAAAAB5TaXplXzMwMC9pMDAwMDAwMDA3MTYwXzMwMC5qcGcGBQAAAAVBcHBsZQYGAAAAD2lQaG9uZSA3ICgzMmdiKQYHAAAABDMyZ2IGCAAAAA1Nb2JpbGUgcGhvbmVzCgseDEludENvbmRpdGlvbgIFHg9TZWxlY3RlZE5ldHdvcmsFCFVubG9ja2VkZBYCAgEPZBYCZg9kFjICAQ8WAh4Dc3JjBVFodHRwczovL2ltYWdlcy5tdXNpY21hZ3BpZS5jby51ay9pbWFnZXMvdGVjaGltYWdlcy9TaXplXzMwMC9pMDAwMDAwMDA3MTYwXzMwMC5qcGdkAgMPDxYCHwAFFUFwcGxlIGlQaG9uZSA3ICgzMmdiKWRkAgcPDxYCHwAFBjIxNS4wMGRkAgkPFgIfDgVRaHR0cHM6Ly9pbWFnZXMubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzL3RlY2hpbWFnZXMvU2l6ZV8zMDAvaTAwMDAwMDAwNzE2MF8zMDAuanBnZAINDxAPFgIfAWdkDxYKZgIBAgICAwIEAgUCBgIHAggCCRYKEAUIVW5sb2NrZWQFATBnEAUCTzIFAThnEAUCRUUFATJnEAUIVm9kYWZvbmUFATVnEAUGT3JhbmdlBQExZxAFCFQtTW9iaWxlBQEzZxAFATMFATZnEAUGVmlyZ2luBQE0ZxAFBVRlc2NvBQE3ZxAFB1Vua25vd24FATlnFgFmZAIPD2QWAgIDDxYCHgtfIUl0ZW1Db3VudAIKFhRmD2QWAgIBDw8WAh4PQ29tbWFuZEFyZ3VtZW50BQEwFgIeB2RhdGEtaWQFATAWAmYPFgQeBWNsYXNzBSRpdGVtQ29uZGl0aW9uTmV0d29ya2VkQnV0dG9uU2VsZWN0ZWQfDgU7aHR0cDovL3d3dy5tdXNpY21hZ3BpZS5jby51ay9pbWFnZXMvVW5sb2NrZWRfVW5zZWxlY3RlZC5wbmdkAgEPZBYCAgEPDxYCHxAFATgWAh8RBQE4FgJmDxYCHw4FNWh0dHA6Ly93d3cubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzL08yX1Vuc2VsZWN0ZWQucG5nZAICD2QWAgIBDw8WAh8QBQEyFgIfEQUBMhYCZg8WAh8OBTVodHRwOi8vd3d3Lm11c2ljbWFncGllLmNvLnVrL2ltYWdlcy9FRV9VbnNlbGVjdGVkLnBuZ2QCAw9kFgICAQ8PFgIfEAUBNRYCHxEFATUWAmYPFgIfDgU7aHR0cDovL3d3dy5tdXNpY21hZ3BpZS5jby51ay9pbWFnZXMvVm9kYWZvbmVfVW5zZWxlY3RlZC5wbmdkAgQPZBYCAgEPDxYCHxAFATEWAh8RBQExFgJmDxYCHw4FOWh0dHA6Ly93d3cubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzL09yYW5nZV9VbnNlbGVjdGVkLnBuZ2QCBQ9kFgICAQ8PFgIfEAUBMxYCHxEFATMWAmYPFgIfDgU7aHR0cDovL3d3dy5tdXNpY21hZ3BpZS5jby51ay9pbWFnZXMvVC1Nb2JpbGVfVW5zZWxlY3RlZC5wbmdkAgYPZBYCAgEPDxYCHxAFATYWAh8RBQE2FgJmDxYCHw4FNGh0dHA6Ly93d3cubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzLzNfVW5zZWxlY3RlZC5wbmdkAgcPZBYCAgEPDxYCHxAFATQWAh8RBQE0FgJmDxYCHw4FOWh0dHA6Ly93d3cubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzL1Zpcmdpbl9VbnNlbGVjdGVkLnBuZ2QCCA9kFgICAQ8PFgIfEAUBNxYCHxEFATcWAmYPFgIfDgU4aHR0cDovL3d3dy5tdXNpY21hZ3BpZS5jby51ay9pbWFnZXMvVGVzY29fVW5zZWxlY3RlZC5wbmdkAgkPZBYCAgEPDxYCHxAFATkWAh8RBQE5FgJmDxYCHw4FOmh0dHA6Ly93d3cubXVzaWNtYWdwaWUuY28udWsvaW1hZ2VzL1Vua25vd25fVW5zZWxlY3RlZC5wbmdkAhMPDxYEHghDc3NDbGFzcwUbaXRlbUNvbmRpdGlvbkJ1dHRvblNlbGVjdGVkHgRfIVNCAgJkZAIVDw8WBB8TBR1pdGVtQ29uZGl0aW9uQnV0dG9uVW5zZWxlY3RlZB8UAgJkZAIXDw8WBB8TBR1pdGVtQ29uZGl0aW9uQnV0dG9uVW5zZWxlY3RlZB8UAgJkZAIaDw8WAh8ABQVHb29kOmRkAhwPFgQfAAV+PHAgY2xhc3M9J2l0ZW1Db25kaXRpb25Db25kaXRpb25EZXNjcmlwdGlvbkhlYWRlcic+WW91IGRvbuKAmXQgbmVlZCB0byBzZW5kIHlvdXIgY2hhcmdlciwgYWNjZXNzb3JpZXMgb3IgdGhlIG9yaWdpbmFsIGJveCE8L3A+HwFnZAIeDxYEHw8CBB8BZxYIAgEPZBYCAgMPFgIfAAUdRXZlcnl0aGluZyB3b3JrcyBhcyBpdCBzaG91bGRkAgIPZBYCAgMPFgIfAAU8Tm8gbWFqb3IgZGFtYWdlIChpLmUgY2hpcHMgb3IgY3JhY2tzIHRvIHRoZSBzY3JlZW4gb3IgcGhvbmUpZAIDD2QWAgIDDxYCHwAFD05vIHdhdGVyIGRhbWFnZWQCBA9kFgICAw8WAh8ABR5MaWdodCB3ZWFyIGFuZCB0ZWFyIGFjY2VwdGFibGVkAiAPFgIfAWhkAiIPFgIfAWhkAiQPFgIfAWhkAiYPFgIfAWhkAigPFgIfAWhkAioPDxYCHwAFCMKjMjE1LjAwZGQCLg8WAh8BaGQCNA9kFgICAg8PFgIfAAUVQXBwbGUgaVBob25lIDcgKDMyZ2IpZGQCNg9kFgICAg8PFgIfAAUEMzJnYmRkAjgPZBYCAgIPDxYCHwAFCFVubG9ja2VkZGQCOg9kFgICAg8PFgIfAAUER29vZGRkAjwPDxYCHwAFCMKjMjE1LjAwZGQCQg8WAh8BaGRk0O7jBPaz/m9k1oKFXdNCNxCa3x0=',
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        '__SCROLLPOSITIONX': '0',
        '__SCROLLPOSITIONY': '0',
        '__ASYNCPOST': 'true'
    }
    web_data = requests.post(url, headers=header, data=post_data).text
    html = BeautifulSoup(web_data,'lxml')
    #print(html)
    return html

def get_phone_detils(phone_url):
    web_data = get_html(phone_url)
    soup = BeautifulSoup(web_data,'lxml')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    device_model = soup.select('span.itemConditionItemDescription')[0].text
    provider = 'Music Magpie'
    print(date)
    print(device_model)
    print(provider)

    #获取所有的condition的ajax和condition的name
    itemConditionConditionButtonBlocks = soup.select('.itemConditionConditionButtonBlock div a')
    condition_list = []
    condition_name_list = []
    for i in itemConditionConditionButtonBlocks:
        condition_EVENTTARGET = i.get('href').split('\'')[1]
        condition_list.append(condition_EVENTTARGET)
        condition_name_list.append(i.text)
        print(condition_EVENTTARGET)


    #获取所有的网络表单提交参数__EVENTTARGET
    networks_EVENTTARGET_list = []
    itemConditionNetworkPicks = soup.select('.itemConditionNetworkPick a')
    for each in itemConditionNetworkPicks:
        networks_EVENTTARGET = each.get('href').split('\'')[1]
        networks_EVENTTARGET_list.append(networks_EVENTTARGET)
        print(networks_EVENTTARGET)

    #获取所有网络选项为一个list
    networks_options = soup.select('.itemConditionNetworksWrapper option')
    option_list = []
    num_list = []
    for option in networks_options:
        print(option.text)
        option_list.append(option.text)
        num_list.append(option.get('value'))


    for x,name in zip(condition_list,condition_name_list):
        for m,n,num in zip(option_list,networks_EVENTTARGET_list,num_list):
            html = get_data(phone_url,x,num)
            print(m)
            price = html.select('.offerPricePrice')[0].text
            print(price)
            data = {
                'date':date,
                'deviceModel':device_model,
                'provider':provider,
                'condition':name,
                'networks':m,
                'quote':price[1:],
            }
            print(data)
            with open('data2.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['date', 'deviceModel', 'provider', 'condition', 'networks', 'quote']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(data)
                csvfile.close()
            print(data)

# get_phone_detils('https://www.musicmagpie.co.uk/start-selling/basket-condition-alt?barcode=i000000007160')
# url = 'https://www.musicmagpie.co.uk/start-selling/basket-condition-alt?barcode=i000000007160'
# web_data = get_html(url)
# print(web_data)

# EVENTTARGET = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$RptNetwork$ctl00$NetworkBtn'
# url = 'https://www.musicmagpie.co.uk/start-selling/basket-condition-alt?barcode=i000000007160'
# html = get_data(url,'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition3_10$PoorBut',2)
# price = html.select('.offerPricePrice')[0].text
# print(price)

def main():
    url = 'https://www.musicmagpie.co.uk/start-selling/basket-condition-alt?barcode=i000000007160'
    save_to_csv()
    get_phone_detils(url)

if __name__ == '__main__':
    main()

