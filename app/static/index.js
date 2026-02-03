function startup(){
    bindSubmitBtn();
    renderindex();
}

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

async function renderindex(){
    const first_divider = document.getElementById('first-divider');
    try{
        const res = await fetch("/api/get-post");
        const body = await res.json();
        console.log(body);
        if (!body){
            const msg = document.createElement('h3');
            msg.textContent = '尚無貼文';
            return
        }else{
            body.forEach((b) => {
                const container = document.createElement('div');
                const content = document.createElement('div');
                const img = document.createElement('img');
                const divider = document.createElement('hr');

                content.textContent = b.content;
                img.src = b.image_url;
                divider.classList.add('divider');
                container.appendChild(content);
                container.appendChild(img);
                container.appendChild(divider);
                first_divider.after(container);
            });
        }
    }catch(e){
        console.log(e);
    }
    
}

startup();