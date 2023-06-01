import React, {useState} from 'react';
import './styles/app.css';
import {Link, useNavigate, useParams } from "react-router-dom";

const CreatePet = () => {

    const [petName, setPetName] = useState('')
    const [description, setDescription] = useState('')
    const [file, setFile] = useState(null)
    const [animalType, setAnimalType] = useState('')
    const [breed, setBreed] = useState('')
    const [temperment, setTemperment] = useState('')
    const [size, setSize]= useState('')
    const navigate = useNavigate()
    const {userId} = useParams()





    const handleAddPet = () => {

        const formData = new FormData()
        
        if (file === null || description==='' || animalType=== '' || temperment==='' || petName==='' || size==='') {
            alert("You failed to enter necessary information")
            console.log(file, description, animalType, temperment, petName, size)
            return
        } 
        formData.append('image', file);
        formData.append('name', petName)
        formData.append('description', description)
        formData.append('animal', animalType)

        formData.append('temperment', temperment)
        formData.append('size', size)

        // User_Pets - post
        fetch(`/api/user/pets/${userId}`, {
            method: 'POST',
            body: formData
        })
        .then(r =>{
            if(!r.ok){
                throw new Error(r.statusText)
            }
            navigate(`/`)
        })
    }

  
  
    return (
        <div class="upload-container">
            <label for='image'>Choose File:</label>
            <input type='file' onChange={(e)=> setFile((file)=> e.target.files[0])} accept="image/*" />
                
            {file && (
                <div> 
                    <img src={URL.createObjectURL(file)} alt='preview' />
                </div>
            )}
            <h2>Add Pet:</h2>
            <label for='name'>Name</label>
            <input type='text' value={petName} onChange={(e)=> setPetName((petName)=> e.target.value)} />
            <label for='description'>Description</label>
            <textarea rows={4} cols={60} maxLength={200} onChange={(e)=> setDescription((description)=> e.target.value)} />
            <label for="animalType">Animal Type:</label>
            <select value={animalType} onChange={e=> setAnimalType((animalType)=>e.target.value)} name="animalType">
                <option value="">--Please choose an option--</option>
                <option value="Dog">Dog</option>
                <option value="Cat">Cat</option>
                <option value="Bird">Bird</option>
                <option value="Rodent">Rodent</option>
                <option value="Fish">Fish</option>
                <option value="Reptile">Rodent</option>
                <option value="Other">Rodent</option>
            </select>   

            <label for="temperment">Temperment:</label>
                <select value={temperment} onChange={e => setTemperment((temperment)=>e.target.value)} name="temperment">
                <option value="">--Please choose an option--</option>
                <option value="Energetic">Energetic</option>
                <option value="Timid">Timid</option>
                <option value="Agressive">Agressive</option>
                <option value="Affectionate">Affectionate/Latin</option>
                <option value="Independent">Independent</option>
                <option value="Other">Other</option>
            </select>

            <label for="size">Size:</label>
            <select value={size} onChange={e => setSize((size) => e.target.value)} name="relStatus">
                <option value="">--Please choose an option--</option>
                <option value="Extra Small">Extra Smal</option>
                <option value="Small">Small</option>
                <option value="Medium">Medium</option>
                <option value="Large">Large</option>
                <option value="Extra Large">Extra Large</option>
                .
            </select>

            
            <button onClick={handleAddPet}>Update Account</button>
        </div>

  );
};

export default CreatePet;