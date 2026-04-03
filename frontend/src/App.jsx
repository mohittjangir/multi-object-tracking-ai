import { useState } from "react"

export default function App(){

const [file,setFile] = useState(null)

const [inputVideo,setInputVideo] = useState("")

const [outputVideo,setOutputVideo] = useState("")

const [loading,setLoading] = useState(false)

const handleFile = (e)=>{

const selected = e.target.files[0]

setFile(selected)

setInputVideo(

URL.createObjectURL(selected)

)

}

const uploadVideo = async ()=>{

if(!file){

alert("Please select video")

return

}

setLoading(true)

const formData = new FormData()

formData.append("file", file)

const response = await fetch(

"https://YOUR-RENDER-URL.onrender.com/track",

{

method:"POST",

body: formData

}

)

const data = await response.json()

setOutputVideo(

"https://YOUR-RENDER-URL.onrender.com/" + data.output

)

setLoading(false)

}

return(

<div className="container">

<h1>Multi Object Detection & Tracking</h1>

<p>Upload sports video to track players with unique ID</p>

<input

type="file"

accept="video/*"

onChange={handleFile}

/>

<br/>

<button onClick={uploadVideo}>

Process Video

</button>

{loading && <p>Processing video...</p>}

{inputVideo && (

<div>

<h3>Input Video</h3>

<video controls width="450">

<source src={inputVideo} />

</video>

</div>

)}

{outputVideo && (

<div>

<h3>Tracked Output</h3>

<video controls width="450">

<source src={outputVideo} />

</video>

</div>

)}

</div>

)

}