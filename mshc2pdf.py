# import pdfkit
import glob
import zipfile
import os
from bs4 import BeautifulSoup

extract_to = './extracted'

print('Specify a folder with documentation files. It usually contains .mshc, .mshi and .metadata files. Example:')
print(r'C:\ProgramData\Microsoft\HelpLibrary2\Catalogs\VisualStudio15\ContentStore\EN-US')
path = input('> ')#.replace('\\', '/')
#if not path.endswith('/'):
#    path += '/'

mshc_archives = glob.glob(f'{path}*.mshc')

if len(mshc_archives) == 0:
    exit('[-] Can\'t find any .mshc files!')

if not os.path.exists(extract_to):
    os.makedirs(extract_to)


print('Extracting mshc archives... ', end='')
for archive in mshc_archives:
    if not zipfile.is_zipfile(archive):
        print('[!] '+ archive.rsplit('/')[0] + ' is not a valid archive!')
    else:
        with zipfile.ZipFile(archive, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
print('Done.')


print('Renaming files; might take some time... ', end='')
for html_file in glob.glob(f'{extract_to}/*.html'):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    meta = soup.head.find_all('meta')
    #print(meta)

    for m in meta:
        if m.has_attr('name') and m['name'] == 'Title':
            title = m['content'].replace('/', '_')
            #print(f'Renaming {html_file} to {extract_to}/{title}.html')
            os.rename(html_file, f'{extract_to}/{title}.html')
            break
print('Done.')
