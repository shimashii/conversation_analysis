//ここに音声認識の処理を書いていく
var stack = "";
const speech = new webkitSpeechRecognition();
speech.lang = 'ja-JP';

var autotext = "";

const btn = document.getElementById('btn');
const content = document.getElementById('content');

btn.addEventListener('click' , function() {
    // 音声認識をスタート
    speech.start();
});

//音声自動文字起こし機能
speech.onresult = function(e) {
     speech.stop();
     if(e.results[0].isFinal){
         autotext =  e.results[0][0].transcript
         console.log(autotext);
         stack += autotext + " ";
         console.log(stack);
         content.innerHTML += '<div>'+ autotext +'</div>';
      }
 }

 speech.onend = () => { 
    speech.start() 
 };


// 30秒ごとに音声を取得する
setInterval("textPost()", 30000);

var response = null;
var topic = "";

function textPost(){

    let request = {text : stack};
    //ajax
    $.ajax({
        type: "post",
        url: "via.phpを指定",    // 適切なディレクトリを指定ください。
        data        :  request,
        success     : function(data) {
            var regexp = new RegExp(/\[\"\[(.*?)\]\"\]/);
            response = data.match( regexp );
            console.log(response[1])
            topic = response[1]

        },error       : function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("リクエスト時になんらかのエラーが発生しました\n" + url + "\n" + textStatus +":\n" + errorThrown);
        }
    });

    stack = "";
}