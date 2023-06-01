import React, {useState, useEffect} from 'react';
import './styles/app.css';
import {Link, Navigate, useNavigate, useParams } from "react-router-dom";

const ImageUpload = () => {

    const [file, setFile] = useState(null)
    const [description, setDescription] = useState(null)
    const {userId, petId} = useParams()
    const navigate = useNavigate()



    const handleUserImage = () => {
        //User_Photos - post
        const formData = new FormData()
        formData.append('image', file)
        formData.append('description', description)
        fetch(`/api/user/photos/${userId}`, {
            method: 'POST',
            body: formData,
        })
        .then(r => {
            if(!r.ok){
                throw new Error(r.statusText)
            }
            navigate(`/profile/${userId}`)
        })
        
    }

  
  
    return (
        <div class="upload-container">
            <h1>Upload A New Photo</h1>
            <input type="file" onChange={(e)=>setFile((file)=> e.target.files[0])} accept="image/*"  />
            {file && (
                <div>
                    <img className='preview-image' src={URL.createObjectURL(file) } alt='preview' />
                </div>
            )}
            <h3>Description:</h3>
            <input type='text' onChange={(e) => setDescription((description)=> e.target.value)} />
            <button onClick={handleUserImage}>Upload</button>
            
        </div>

  );
};

export default ImageUpload;