const fs = require('fs');
const path = require('path');
const chai = require("chai");
const should = chai.should();
const JWebDriver = require('jwebdriver');
chai.use(JWebDriver.chaiSupportChainPromise);
const resemble = require('resemblejs-node');
resemble.outputSettings({
    errorType: 'flatDifferenceIntensity'
});

const rootPath = getRootPath();

module.exports = function(){

    let driver, testVars;

    before(function(){
        let self = this;
        driver = self.driver;
        testVars = self.testVars;
    });

    it('url: http://127.0.0.1:8000/taskList/', async function(){
        await driver.url(_(`http://127.0.0.1:8000/taskList/`));
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 新增项目 ( //a[text()="新增项目"], 47, 33, 0 )', async function(){
        await driver.sleep(300).wait('//a[text()="新增项目"]', 30000)
               .sleep(300).mouseMove(47, 33).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 项目名称 ( #projectName, 40, 13, 0 )', async function(){
        await driver.sleep(300).wait('#projectName', 30000)
               .sleep(300).mouseMove(40, 13).click(0);
    });

    it('sendKeys: xiang{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}项目名称1', async function(){
        await driver.sendKeys('xiang{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}{BACK_SPACE}项目名称1');
    });

    it('click: 项目管理地址 ( #projectUrl, 49, 17, 0 )', async function(){
        await driver.sleep(300).wait('#projectUrl', 30000)
               .sleep(300).mouseMove(49, 17).click(0);
    });

    it('sendKeys: 项目1地址', async function(){
        await driver.sendKeys('项目1地址');
    });

    it('click: 提交 ( //button[text()="提交"], 35, 15, 0 )', async function(){
        await driver.sleep(300).wait('//button[text()="提交"]', 30000)
               .sleep(300).mouseMove(35, 15).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 新增计划 ( //a[text()="新增计划"], 60, 31, 0 )', async function(){
        await driver.sleep(300).wait('//a[text()="新增计划"]', 30000)
               .sleep(300).mouseMove(60, 31).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 测试计划名称 ( #planName, 55, 16, 0 )', async function(){
        await driver.sleep(300).wait('#planName', 30000)
               .sleep(300).mouseMove(55, 16).click(0);
    });

    it('sendKeys: 项目1-计划1', async function(){
        await driver.sendKeys('项目1-计划1');
    });

    it('click: 提交 ( //button[text()="提交"], 33, 19, 0 )', async function(){
        await driver.sleep(300).wait('//button[text()="提交"]', 30000)
               .sleep(300).mouseMove(33, 19).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 新增轮次 ( //a[text()="新增轮次"], 57, 38, 0 )', async function(){
        await driver.sleep(300).wait('//a[text()="新增轮次"]', 30000)
               .sleep(300).mouseMove(57, 38).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    it('click: 测试轮次名称 ( #turnName, 53, 14, 0 )', async function(){
        await driver.sleep(300).wait('#turnName', 30000)
               .sleep(300).mouseMove(53, 14).click(0);
    });

    it('sendKeys: 项目1-计划1-轮次1', async function(){
        await driver.sendKeys('项目1-计划1-轮次1');
    });

    it('click: 测试内容概要 ( #content, 37, 28, 0 )', async function(){
        await driver.sleep(300).wait('#content', 30000)
               .sleep(300).mouseMove(37, 28).click(0);
    });

    it('sendKeys: 内容1', async function(){
        await driver.sendKeys('内容1');
    });

    it('click: 测试人员 ( #tester, 51, 10, 0 )', async function(){
        await driver.sleep(300).wait('#tester', 30000)
               .sleep(300).mouseMove(51, 10).click(0);
    });

    it('sendKeys: 人员1', async function(){
        await driver.sendKeys('人员1');
    });

    it('click: 开始时间 ( #startTime, 35, 26, 0 )', async function(){
        await driver.sleep(300).wait('#startTime', 30000)
               .sleep(300).mouseMove(35, 26).click(0);
    });

    it('sendKeys: 2017-09-07', async function(){
        await driver.sendKeys('2017-09-07');
    });

    it('click: 结束时间 ( #endTime, 31, 15, 0 )', async function(){
        await driver.sleep(300).wait('#endTime', 30000)
               .sleep(300).mouseMove(31, 15).click(0);
    });

    it('sendKeys: 2017-09-10', async function(){
        await driver.sendKeys('2017-09-10');
    });

    it('click: 工时 ( #workHour, 57, 15, 0 )', async function(){
        await driver.sleep(300).wait('#workHour', 30000)
               .sleep(300).mouseMove(57, 15).click(0);
    });

    it('sendKeys: 11', async function(){
        await driver.sendKeys('11');
    });

    it('click: 备注 ( #mark, 40, 14, 0 )', async function(){
        await driver.sleep(300).wait('#mark', 30000)
               .sleep(300).mouseMove(40, 14).click(0);
    });

    it('sendKeys: 11', async function(){
        await driver.sendKeys('11');
    });

    it('click: 提交 ( //button[text()="提交"], 38, 21, 0 )', async function(){
        await driver.sleep(300).wait('//button[text()="提交"]', 30000)
               .sleep(300).mouseMove(38, 21).click(0);
    });

    it('waitBody: ', async function(){
        await driver.sleep(500).wait('body', 30000).html().then(function(code){
            isPageError(code).should.be.false;
        });
    });

    function _(str){
        if(typeof str === 'string'){
            return str.replace(/\{\{(.+?)\}\}/g, function(all, key){
                return testVars[key] || '';
            });
        }
        else{
            return str;
        }
    }

};

if(module.parent && /mocha\.js/.test(module.parent.id)){
    runThisSpec();
}

function runThisSpec(){
    // read config
    let webdriver = process.env['webdriver'] || '';
    let proxy = process.env['wdproxy'] || '';
    let config = require(rootPath + '/config.json');
    let webdriverConfig = Object.assign({},config.webdriver);
    let host = webdriverConfig.host;
    let port = webdriverConfig.port || 4444;
    let match = webdriver.match(/([^\:]+)(?:\:(\d+))?/);
    if(match){
        host = match[1] || host;
        port = match[2] || port;
    }
    let testVars = config.vars;
    let browsers = webdriverConfig.browsers;
    browsers = browsers.replace(/^\s+|\s+$/g, '');
    delete webdriverConfig.host;
    delete webdriverConfig.port;
    delete webdriverConfig.browsers;

    // read hosts
    let hostsPath = rootPath + '/hosts';
    let hosts = '';
    if(fs.existsSync(hostsPath)){
        hosts = fs.readFileSync(hostsPath).toString();
    }
    let specName = path.relative(rootPath, __filename).replace(/\\/g,'/').replace(/\.js$/,'');

    browsers.split(/\s*,\s*/).forEach(function(browserName){
        let caseName = specName + ' : ' + browserName;

        let browserInfo = browserName.split(' ');
        browserName = browserInfo[0];
        let browserVersion = browserInfo[1];

        describe(caseName, function(){

            this.timeout(600000);
            this.slow(1000);

            let driver;
            before(function(){
                let self = this;
                let driver = new JWebDriver({
                    'host': host,
                    'port': port
                });
                let sessionConfig = Object.assign({}, webdriverConfig, {
                    'browserName': browserName,
                    'version': browserVersion,
                    'ie.ensureCleanSession': true,
                    'chromeOptions': {
                        'args': ['--enable-automation']
                    }
                });
                if(proxy){
                    sessionConfig.proxy = {
                        'proxyType': 'manual',
                        'httpProxy': proxy,
                        'sslProxy': proxy
                    }
                }
                else if(hosts){
                    sessionConfig.hosts = hosts;
                }
                self.driver = driver.session(sessionConfig).maximize().config({
                    pageloadTimeout: 30000, // page onload timeout
                    scriptTimeout: 5000, // sync script timeout
                    asyncScriptTimeout: 10000 // async script timeout
                });
                self.testVars = testVars;
                let casePath = path.dirname(caseName);
                self.screenshotPath = rootPath + '/screenshots/' + casePath;
                self.diffbasePath = rootPath + '/diffbase/' + casePath;
                self.caseName = caseName.replace(/.*\//g, '').replace(/\s*[:\.\:\-\s]\s*/g, '_');
                mkdirs(self.screenshotPath);
                mkdirs(self.diffbasePath);
                self.stepId = 0;
                return self.driver;
            });

            module.exports();

            beforeEach(function(){
                let self = this;
                self.stepId ++;
                if(self.skipAll){
                    self.skip();
                }
            });

            afterEach(async function(){
                let self = this;
                let currentTest = self.currentTest;
                let title = currentTest.title;
                if(currentTest.state === 'failed' && /^(url|waitBody|switchWindow|switchFrame):/.test(title)){
                    self.skipAll = true;
                }
                if(!/^(closeWindow):/.test(title)){
                    let filepath = self.screenshotPath + '/' + self.caseName + '_' + self.stepId;
                    let driver = self.driver;
                    try{
                        // catch error when get alert msg
                        await driver.getScreenshot(filepath + '.png');
                        let url = await driver.url();
                        let html = await driver.source();
                        html = '<!--url: '+url+' -->\n' + html;
                        fs.writeFileSync(filepath + '.html', html);
                        let cookies = await driver.cookies();
                        fs.writeFileSync(filepath + '.cookie', JSON.stringify(cookies));
                    }
                    catch(e){}
                }
            });

            after(function(){
                return this.driver.close();
            });

        });
    });
}

function getRootPath(){
    let rootPath = path.resolve(__dirname);
    while(rootPath){
        if(fs.existsSync(rootPath + '/config.json')){
            break;
        }
        rootPath = rootPath.substring(0, rootPath.lastIndexOf(path.sep));
    }
    return rootPath;
}

function mkdirs(dirname){
    if(fs.existsSync(dirname)){
        return true;
    }else{
        if(mkdirs(path.dirname(dirname))){
            fs.mkdirSync(dirname);
            return true;
        }
    }
}

function callSpec(name){
    try{
        require(rootPath + '/' + name)();
    }
    catch(e){
        console.log(e)
        process.exit(1);
    }
}

function isPageError(code){
    return code == '' || / jscontent="errorCode" jstcache="\d+"|diagnoseConnectionAndRefresh|dnserror_unavailable_header|id="reportCertificateErrorRetry"|400 Bad Request|403 Forbidden|404 Not Found|500 Internal Server Error|502 Bad Gateway|503 Service Temporarily Unavailable|504 Gateway Time-out/i.test(code);
}

function catchError(error){

}
