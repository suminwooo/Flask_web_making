   //request json
        let request = obj => {
            return new Promise((resolve, reject) => {
                let xhr = new XMLHttpRequest();
                xhr.open(obj.method || "GET", obj.url);
                if (obj.headers) {
                    Object.keys(obj.headers).forEach(key => {
                        xhr.setRequestHeader(key, obj.headers[key]);
                    });
                }
                xhr.onload = () => {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        var resp = xhr.responseText;
                        var respJson = JSON.parse(resp);
                        resolve(respJson);
                    } else {
                        reject(xhr.statusText);
                    }
                };
                xhr.onerror = () => reject(xhr.statusText);
                xhr.send(obj.body);
            });
        };

    function buildTable(obj, el) {
        console.log('obj',obj.querySet)
        console.log('el',el)
        //trim view data
        let trimStart = (obj.page - 1) * obj.rows
        let trimEnd = trimStart + obj.rows
        let trimmedData = Object.fromEntries(
            Object.entries(obj.querySet).slice(trimStart, trimEnd)
        )

        //total view pages
        obj.pages = Math.ceil(Object.keys(obj.querySet).length / obj.rows)
        el.innerHTML = ""

        for (const prop in trimmedData) {
            let item = trimmedData[prop];

            let childItems = Object.values(trimmedData[prop]);
            console.log('item', childItems)

            let row = `<tr>`
            for (let i = 0; i < childItems.length; i++) {

               row += `<td>${childItems[i]}</td>`

            }
            row += `</tr>`

            el.insertAdjacentHTML('beforeend', row)

        }
    }


    //set numbered buttons into pagination
    function setPaginationButton(pEl, obj, tEl) {

        for (let i = obj.page; i <= obj.window; i++) {
            let btn = PaginationButton(i , obj, tEl)
            var total = i
            pEl.appendChild(btn);
        }

        if (total < obj.pages) setNextButton(pEl, obj, tEl)
        if (obj.page > 1) setPrevButton(pEl, obj, tEl)

    }

    //create next button
    function setNextButton(p, obj, t) {
        let nextButton = document.createElement('button');
        nextButton.innerText = `>>`
        nextButton.value = obj.window + 5

        nextButton.addEventListener('click', function () {
            console.log('next')
            obj.page = obj.window + 1
            obj.window = obj.window + 5
            p.innerText = ''

            buildTable(obj, t)
            setPaginationButton(p, obj, t);
        });

        p.appendChild(nextButton);
    }

    //create prev button
    function setPrevButton(p, obj, t) {
        let prevButton = document.createElement('button');
        prevButton.innerText = `<<`
        prevButton.value = obj.window - 5

        prevButton.addEventListener('click', function () {
            console.log('prev')
            obj.page = obj.page - 5
            obj.window = obj.window - 5
            p.innerText = ''

            buildTable(obj, t)
            setPaginationButton(p, obj, t);
        });

        p.prepend(prevButton);
    }

    // create button
    function PaginationButton(page, obj, el) {
        let button = document.createElement('button');
        console.log('page',page)
        button.innerText = page;
        button.value = page;

        button.addEventListener('click', function () {
            console.log('click')
            console.log('value', this.value)
            el.innerHTML = ``;
            obj.page = this.value
            buildTable(obj, el)
        });

        return button;
    }