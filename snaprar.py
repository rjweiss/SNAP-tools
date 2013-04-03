import tldextract
import rarfile
import os 
import sys
import tempfile
import shutil
import gzip


def newitem(name):
    return {
        'file': name,
        'url': '__nourl__',
        'date': '__nodate__',
        'title': '__notitle__',
        'content': '__nocontent__',
        'links': 0,
        'quotes': 0,
    }

def printitem(ditem):

    if ditem['content'] != '__nocontent__':
        ditem['content'] = str(ditem['content'])

    if ditem['links'] == 0:
        ditem['links'] = '__nolinks__'
    else:
        ditem['links'] = str(ditem['links'])
            
    if ditem['quotes'] == 0:
        ditem['quotes'] = '__noquotes__'
    else:
        ditem['quotes'] = str(ditem['quotes'])

    outline = [
        ditem['file'],
        ditem['url'],
        ditem['date'],
        ditem['title'],
        ditem['content'],
        ditem['links'],
        ditem['quotes'],
    ]

    return '\t'.join(outline)

def domainfilter(urlstring, domains):
	url = tldextract.extract(urlstring)
	if url.domain in domains:
		print url.domain
		return urlstring
	else:
		return False


def process_file(snaptext, domains):
	outfile = []
	snapfile = open(snaptext, 'r')
	ditem = newitem(snaptext)

	for line in snapfile:
		cline = line.split('\n')[0]				
		words = cline.split('\t')

		if len(words) <= 1:

			if ditem['url'] != '__nourl__':
				outfile.append(ditem)

			ditem = newitem(snaptext)

			continue

		key = words[0]
		value = words[1]

		if key == 'U':
			urlfilter = domainfilter(value, domains)
			if urlfilter:
				ditem['url'] = value
			else:
				continue	
		elif key == 'D':
			ditem['date'] = value
		elif key == 'T':
			ditem['title'] = value
		elif key == 'C':
			ditem['content'] = value
		elif key == 'L':
			ditem['links'] += 1
		elif key == 'Q':
			ditem['quotes'] += 1
		else:
			print '*** ERROR: unknown key'
			#sys.exit(1)
	
	return outfile
	
	snapfile.close()

def main():
	
	target_dir = sys.argv[1]

	newsdomains = set([])
	
	with open(sys.argv[2], 'r') as newssites:
		for line in newssites:
			newsdomains.add(line.strip())

	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' + <traversal dir> + <news domains text file>'
		sys.exit(1)

	for item in os.listdir(target_dir):
		item_path = os.path.join(target_dir, item)
		if item.startswith('web-') and rarfile.is_rarfile(item_path):
			rf = rarfile.RarFile(item_path)
			
			try:
			    tmp_dir = tempfile.mkdtemp()
			    rf.extractall(path=tmp_dir)
			    flatsnap = process_file(os.path.join(tmp_dir, rf.namelist()[0]), newsdomains)
			    archive_name = os.path.splitext(rf.namelist()[0])[0] + '_news.gz'
			    with gzip.open(archive_name, 'wb') as archive:
			    	for item in flatsnap:
			    		archive.write('%s\n' % item)
			finally:
			    try:
				shutil.rmtree(tmp_dir)
			    except OSError, e:
				if e.errno != 2: # code 2 - no such file or directory
				    raise
		
	
if __name__ == '__main__':
	main()

