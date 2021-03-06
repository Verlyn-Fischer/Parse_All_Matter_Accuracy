import json
import re
import datetime
import csv


def loadAccuracy(filename):
    with open(filename,'r') as jsonFile:
        data = json.load(jsonFile)
    return data

def convertDate(dateString):
    if dateString != None:
        outputDate = datetime.date(int(dateString[0:4]),int(dateString[5:7]),int(dateString[8:10]))
    else:
        outputDate = datetime.date.today()
    return outputDate

def isContract(tag):
    if (len(re.findall('contract',tag))>0 or len(re.findall('Contract',tag))>0) and len(re.findall('contractor',tag))==0:
        return True
    else:
        return False

def isAgreement(tag):
    if len(re.findall('agree',tag))>0 or len(re.findall('Agree',tag))>0:
        return True
    else:
        return False

def isPriv(tag):
    if (len(re.findall('Privilege',tag))>0 or len(re.findall('privilege',tag))>0) and len(re.findall('Not Privilege',tag))==0 \
            and len(re.findall('No Privilege',tag))==0 and len(re.findall('Non-Privilege',tag))==0\
            and len(re.findall('Not privilege',tag))==0 and len(re.findall('Potentially',tag))==0:
        return True
    else:
        return False

def isSpam(tag):
    if len(re.findall('Junk',tag))>0 or len(re.findall('junk',tag))>0 \
            or len(re.findall('spam',tag))>0 or len(re.findall('Spam',tag))>0 \
            or len(re.findall('inappropriate',tag))>0 or len(re.findall('Inappropriate',tag))>0\
            or len(re.findall('trash',tag))>0 or len(re.findall('Trash',tag))>0:
        return True
    else:
        return False

def saveCSV(filename,data):
    with open(filename,'w') as csvFile:
        csvWriter = csv.writer(csvFile,delimiter=',')
        csvWriter.writerows(data)

def main():
    todayDate = datetime.date.today()
    candidates = []
    candidates.append(('matter_id','matter_name', 'ml_id','tag','pos_sig','neg_sig','tn','fp','fn','tp','pos_recall','neg_recall'))
    data = loadAccuracy('allmatter_accuracy_2020-02-18.json')
    for matter in data['matters']:
        if 'last_tagged_at' in data['matters'][matter]:
            last_tagged = convertDate(data['matters'][matter]['last_tagged_at'])
            if todayDate - last_tagged > datetime.timedelta(days=30):
                if 'latest_perceived_accuracies' in data['matters'][matter]:
                    for tag in data['matters'][matter]['latest_perceived_accuracies']:
                        if isPriv(tag):
                            pos_signals = data['matters'][matter]['latest_perceived_accuracies'][tag]['pos_signals']
                            neg_signals = data['matters'][matter]['latest_perceived_accuracies'][tag]['neg_signals']
                            tn = data['matters'][matter]['latest_perceived_accuracies'][tag]['tn']
                            fp = data['matters'][matter]['latest_perceived_accuracies'][tag]['fp']
                            fn = data['matters'][matter]['latest_perceived_accuracies'][tag]['fn']
                            tp = data['matters'][matter]['latest_perceived_accuracies'][tag]['tp']
                            if tp + fn > 0:
                                pos_recall = tp / (tp + fn)
                            else:
                                pos_recall = 0
                            if fp + tn > 0:
                                neg_recall = tn / (fp + tn)
                            else:
                                neg_recall = 0
                            if pos_signals > 1000 and neg_signals > 1000:
                                matter_id = matter
                                matter_name = data['matters'][matter]['matter_name']
                                ml_id = data['matters'][matter]['matter_id']
                                tag_name = tag
                                candidates.append((matter_id, matter_name, ml_id, tag_name,pos_signals,neg_signals,tn,fp,fn,tp,pos_recall,neg_recall))
    saveCSV('matters_with_priv_addl.csv',candidates)

main()