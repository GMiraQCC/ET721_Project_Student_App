// Authentication
function validatePasswordLength(){
    const password = document.querySelector('input[name="password"]').value
    
    if (password.length < 6){
        alert("Passowrd must be at least 6 characters long!")
        return false
    }

    return true
}



// Tasks
function loadTasks(){
    fetch("/get_tasks")
        .then(response => response.json())
        .then(data => {
            const list = document.querySelector("#taskList");
            list.innerHTML = "";

            data.forEach(task => {
                createTaskElement(task.id, task.task, task.category, task.due, task.remind);
            });
        });
}

function addTask(){
    const task = document.querySelector('#addTaskTitle').value
    const category = document.querySelector('#addTaskCategory').value
    const due = document.querySelector('#addTaskDue').value
    const remind = document.querySelector('#addTaskRemind').value

    if(!task) return;

    fetch("/add_task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task: task, category: category, due: due, remind: remind})
    })
    .then(()=>{
        document.querySelector('#addTaskTitle').value = "";
        document.querySelector('#addTaskCategory').value = "academic";
        document.querySelector('#addTaskDue').value = "";
        document.querySelector('#addTaskRemind').value = "";
        loadTasks();
    })
    /* EXTRA shit that I might not have to implement
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success') {
            document.querySelector('#addTaskTitle').value = "";
            loadTasks();
        }
    })
    .catch(error => console.error('Error:', error));
    */
}

function deleteTask(id){
    fetch("/delete_task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: id})
    })

    .then(()=>loadTasks());
}

function createTaskElement(id, task, category, due, remind) {
    const list = document.querySelector("#taskList");
    const li = document.createElement("li");
    
    li.textContent = `${task} ||| ${category} ||| Due: ${due || 'No due date'} ||| Reminder: ${remind || 'No reminder'}`;
    li.classList.add("taskItem");

    const btn = document.createElement("button");
    btn.innerHTML = "&#10060";
    btn.onclick = ()=> deleteTask(id);
    btn.classList.add("btnDeleteItem");

    li.appendChild(btn);
    list.appendChild(li);
}



// Images
document.querySelector('#imgUploadForm').addEventListener('submit', function(e){
    e.preventDefault()

    const fileInput = document.querySelector('#imgInput')
    const subject = document.querySelector('#addImgSubject').value
    const topic = document.querySelector('#addImgTopic').value
    const message = document.querySelector('#message')

    if(!fileInput.files.length){
        message.textContent = "Please select an image!"
        message.style.color = 'red'
        return ;
    }

    const formData = new FormData()
    formData.append('image', fileInput.files[0])
    formData.append('subject', subject)
    formData.append('topic', topic)

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data =>{
        if(data.message){
            // show server success msg
            message.textContent = data.message
            message.style.color = 'green'

            // reload the page after 1s of delay
            setTimeout(()=>{location.reload()}, 1000)
        }
        else{
            message.textContent = data.error || "Upload failed"
            message.color = 'red'
        }
    })
})

function deleteImage(id){
    if(!confirm("Are you sure you want to delete this image?"))
        return;

    fetch(`/delete/${id}` , {
        method: 'DELETE'
    })
    .then(response=>response.json())
    .then(data=>{
        if(data.message){
            document.getElementById(`image-${id}`).remove()
        }
        else{
            alert(data.error)
        }
    })
}