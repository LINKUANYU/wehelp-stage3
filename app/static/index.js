

function bindSubmitBtn(){
    const form = document.getElementById('submit-form');
    form.addEventListener('submit', async(e) => {
        e.preventDefault();

        const formData = new FormData();
        const text = document.getElementById('input-text').value;
        const img = document.getElementById('input-img').files[0];
        if (!text || !img){
            alert('請輸入完整訊息');
            return
        }

        formData.append('content', text);
        formData.append('image', img);

        try{
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const body = await res.json();

            if(res.ok){
                window.location.reload();
            }else{
                console.log("上傳失敗")
            }
        }catch(e){
            console.log(e);
        }

    });
}

bindSubmitBtn()