// Add <script src="common.js"></script> to Use This 
(function () {
    if (document.body.dataset.commonjs == "loaded")
        return console.error("为避免脚本重新加载已强行停止");
    document.body.dataset.commonjs = "loaded";

    try {
        window.commonStorage.test;
    } catch (error) {
        window._commonStorage = new Object();
        Object.defineProperty(window, 'commonStorage', {
            value: window._commonStorage
        })
        console.log("commonStorage 失效,已切换到自定义Object.");
    }
    var stress = function (streesNum) {
        var strnum = '';
        for (let index = 0; index < streesNum; index++) {
            index = parseInt((stress * 10 / 10).toString())
        }
        return strnum
    }
    var dynamicLoadCss = function (url,recogAsContent) {
        var head = document.head;
        var link = document.createElement(recogAsContent?"style":'link');
        
        if(recogAsContent)
        {
            link.type = 'text/css';
            link.rel = 'stylesheet';
            link.innerHTML = url;
        }
        else
            link.href = url;
        link.id = 'commonCss_FromJs';
        head.appendChild(link);
    }
    var updateWallpaper = function () {
        if (commonStorage['wallpaper'] == 'true') {
            document.documentElement.classList.add('wallpaper')
        } else {
            document.documentElement.classList.remove('wallpaper')
        }
        if (commonStorage['nowallpaper'] == 'true') {
            document.documentElement.classList.add('nowallpaper')
        } else {
            document.documentElement.classList.remove('nowallpaper')
        }
    }
    var webcom = function () {
        document.body.onkeydown = (e) => {
            if (e.keyCode == 13) {
                e.preventDefault();
                e.stopPropagation();
                var isShowedAns = !document.getElementById('easebuts').classList.contains('invisible')
                if (isShowedAns) {
                    if (!document.querySelectorAll('#easebuts button')[2]) {
                        document.querySelectorAll('#easebuts button')[1].click();
                    } else {
                        document.querySelectorAll('#easebuts button')[2].click();
                    }
                } else {
                    document.getElementById('ansbuta').click();
                }
            } else {
                var index = e.keyCode - 97;
                document.querySelectorAll('#easebuts button')[index].click();
            }
        } //小键盘答题
        document.documentElement.classList.add('nightMode');
        document.documentElement.classList.add('night_mode');
        document.body.classList.add('nightMode');
        document.body.classList.add('night_mode');
        document.documentElement.style = "background:black !important;";
        console.log('已为网页版anki添加小键盘答题和夜间模式')

    }
    if (!document.querySelector('commonCss_FromJs')) {
        dynamicLoadCss('common.css');
        dynamicLoadCss(`.hide {
            display: none;
        }`,true)
    }
    if (location.href.indexOf('ankiuser') > 0) {
        document.documentElement.classList.add('common_web_mode');
        location.href.indexOf('ankiuser') > 0 && webcom();
        return
    }
    if (document.documentElement.classList.contains('android')) {
        //document.querySelector('.card').classList.add("mathjax-rendered");
        //document.querySelector('.card').classList.add("no_flicker");
        //card.classList.remove("mathjax-needs-to-render");
        //window.onload = ()=>{};//防止闪烁
        updateWallpaper();
        return
    }
    if (document.documentElement.classList.contains('ios')) {
        return
    }
    var node = function (name, nodehtml) {
        var ren = document.createElement(name)
        ren.innerHTML = nodehtml || ''
        return ren
    }
    var $ = function (expression) {
        return document.querySelector(expression)
    }
    var msg_killer = undefined
    var msg = function (messageStr, msTime) {
        //发送相同消息有续命效果 
        var msgbox = $('#common_msg')
        if (msgbox.classList.contains('show')) {
            if (messageStr == msgbox.innerHTML) {
                try {
                    clearTimeout(msg_killer)
                } catch (e) {
                    msgbox.className = 'show'
                }
                msg_killer = setTimeout(() => {
                    msgbox.className = 'hide'
                }, msTime || 2000);
                return true
            }
            return false
        }
        msgbox.className = 'show'
        msgbox.innerHTML = messageStr
        msg_killer = setTimeout(() => {
            msgbox.className = 'hide'
        }, msTime || 2000);
        return true
    }

    if (window.answerMode === undefined) {
        Object.defineProperty(window, "answerMode", {
            get: () => document.documentElement.classList.contains('common_question')
        })
        console.log("加载左右滑动事件");
        //document.addEventListener('touchstart', handleTouchStart, false);
        //document.addEventListener('touchend', handleTouchMove, false);

        var xDown = null;
        var yDown = null;
        var donwTime = null;

        function getTouches(evt) {
            return evt.touches ||             // browser API
                evt.originalEvent.touches; // jQuery
        }

        function handleTouchStart(evt) {

            const firstTouch = getTouches(evt)[0];
            xDown = firstTouch.clientX;
            yDown = firstTouch.clientY;
            donwTime = new Date().getTime();
            evt.stopPropagation();
            //evt.preventDefault();

        };

        function handleTouchEnd(evt) {
            //evt.preventDefault();
            //evt.stopPropagation();

            if (!xDown || !yDown) {
                return;
            }

            var xUp = evt.changedTouches[0].clientX;
            var yUp = evt.changedTouches[0].clientY;

            var xDiff = xDown - xUp;
            var yDiff = yDown - yUp;
            if (new Date().getTime() - donwTime > 350) return;
            if (Math.abs(xDiff) + Math.abs(yDiff) < 20) {//点击
                if (xUp > window.document.body.clientWidth / 3 * 2) {
                    rightClick(evt);
                } else if (xUp < window.document.body.clientWidth / 3) {
                    leftClick(evt);
                }

                return;
            }
            if (Math.abs(yDiff) > 75) return;
            if (Math.abs(xDiff) < 75) return;
            if (Math.abs(xDiff) > Math.abs(yDiff)) {/*most significant*/
                if (xDiff > 0) {
                    /* right to left */
                    console.log("right");
                    rightClick(evt);
                } else {
                    /* left to right */
                    console.log("left");
                    window.pycmd("undo");//由python插件提供
                    //leftClick(evt);
                }
            } else {
                if (yDiff > 0) {
                    /* down swipe */
                } else {
                    /* up swipe */
                }
            }
            /* reset values */
            xDown = null;
            yDown = null;
        };

        document.ontouchstart = handleTouchStart;
        document.ontouchend = handleTouchEnd;
    }

    console.log("answermode:", answerMode);

    if (!document.documentElement.classList.contains('touch_device')) {
        document.documentElement.classList.add('notouch_device')
    }
    //事件定义
    //四个难度分别为 1234
    var cancelEvent = function (e) {
        e.preventDefault()
        e.stopPropagation()
    }
    var leftClick = function (e) {
        if (!answerMode) {
            pycmd('ease1');
        } else {
            pycmd('ans')
        }
        if (!e) return;
        e.stopPropagation()
        e.preventDefault()

    }
    var leftRClick = function (e) {
        pycmd('edit');
        return false
    }
    var rightRClick = function (e) {
        pycmd('more');
        return false
    }
    var rightClick = function (e) {
        if (!answerMode) {
            pycmd('ease3');
            pycmd('ease2');
            //也有可能只有两个难度（上一回合回答不会）
        } else {
            pycmd('ans');
        }
        if (!e) return;
        e.stopPropagation()
        e.preventDefault()

    }
    var upRDlick = function (e) {
        commonStorage['wallpaper'] = 'true'
        commonStorage['nowallpaper'] = 'false'
        updateWallpaper();
        msg('壁纸强制开启');
    }
    var downRDlick = function (e) {
        commonStorage['wallpaper'] = 'false'
        commonStorage['nowallpaper'] = 'true'
        updateWallpaper();
        msg('壁纸强制关闭');
    }
    var menumsg = function (e) {
        //检测全屏触摸事件
        var width_r = document.documentElement.clientWidth / 2 + 200;
        var width_l = document.documentElement.clientWidth / 2 - 200;
        var height_u = document.documentElement.clientHeight / 2 - 200;
        var height_d = document.documentElement.clientHeight / 2 + 200;
        var x = e.clientX;
        var y = e.clientY;
        var rev = undefined
        if (x > width_r) {
            rev = rightRClick(e)
        } else if (x < width_l) {
            rev = leftRClick(e)
        } else if (y < height_u) {
            rev = upRDlick(e)
        } else if (y > height_d) {
            rev = downRDlick(e)
        } else {
            return
        }
        e.preventDefault()
        e.stopPropagation()
        return rev
    }
    var resizeFunc = function (e) {
        var width = document.documentElement.clientWidth;
        if (width > 1100) {
            //电脑模式
            document.documentElement.classList.add('common_pc_mode');
            document.documentElement.classList.remove('common_mobile_mode');
        } else {
            //手机模式
            document.documentElement.classList.add('common_mobile_mode');
            document.documentElement.classList.remove('common_pc_mode');
        }
        if (!$('#left_touch') && 0) {
            var lt = node('div')
            lt.id = 'left_touch'
            lt.className = 'touchcon'
            lt.onclick = cancelEvent
            lt.oncontentmenu = leftRClick
            lt.ondblclick = cancelEvent
            lt.ontouchstart = leftClick
            document.body.appendChild(lt)
        }
        if (!$('#right_touch') && 0) {
            var rt = node('div')
            rt.id = 'right_touch'
            rt.className = 'touchcon'
            rt.onclick = cancelEvent
            rt.oncontentmenu = rightRClick
            rt.ondblclick = cancelEvent
            rt.ontouchstart = rightClick
            document.body.appendChild(rt)
        }
    }
    var touchCheck = function (e) {
        if (document.documentElement.classList.contains('touch_device')) {
            return
        }
        document.documentElement.classList.add('touch_device')
        document.documentElement.classList.remove('notouch_device')
        msg('操作鼠标即可退出平板模式', 1000)
    }
    var mouseCheck = function (e) {
        if ($('#common_msg').innerHTML != '点击此处隐蔽两侧按钮' || $('#common_msg').classList.contains('hide')) {
            return
        }
        document.documentElement.classList.remove('touch_device')
        document.documentElement.classList.add('notouch_device')
        try {
            clearTimeout(msg_killer)
        } catch (e) { }
        $('#common_msg').className = 'hide'
    }
    var mouseCheckPre = function (e) {
        if (document.documentElement.classList.contains('notouch_device') || window.touching) {
            return
        }
        msg('点击此处隐蔽两侧按钮')
    }
    var touchRecord = function (e) {
        try {
            clearTimeout(window.touching)
        } catch (e) { }
        window.touching = setTimeout(() => {
            window.touching = undefined
        }, 1000);
    }
    //内容预运行
    resizeFunc();
    if (!$('#common_msg')) {
        var infonode = node('div', '触摸/双击切换模式<br>左向不会 右向记得<br>左右区右键或者长按 对应编辑卡片和菜单')
        infonode.id = 'common_msg'
        infonode.className = 'hide'
        document.body.appendChild(infonode)
        infonode.onclick = mouseCheck;
        setTimeout(() => {
            infonode.className = 'show'
        }, 500);
        setTimeout(() => {
            infonode.className = 'hide'
        }, 3000);
    }
    //事件挂载
    window.onresize = resizeFunc;
    window.ontouchstart = touchCheck;
    window.ondblclick = mouseCheckPre;
    window.onmousemove = mouseCheckPre;
    window.ontouchend = touchRecord;
    window.oncontextmenu = menumsg;
})();