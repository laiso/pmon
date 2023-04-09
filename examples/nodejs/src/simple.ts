import * as https from 'https';
import * as fs from 'fs';
import { argv } from 'process';

function main() {
    const url = argv[2] || 'https://www.example.com';
    https.get(url, (res: any) => {
        console.log('statusCode:', res.statusCode);
        res.setEncoding('utf8');
        res.pipe(fs.createWriteStream('response.txt'));
    });
}

main();

// vim: set expandtab ts=4 sts=4 sw=4 :