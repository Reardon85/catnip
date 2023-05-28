import React, {useState} from 'react';
import '../index.css';
import {Link } from "react-router-dom";

const NewAccount = ({setNewUser, setUser}) => {

    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [file, setFile] = useState(null);
    const [zipcode, setZipcode] = useState(null);
    const [birthday, setBirthday] = useState(null)
    const [gender, setGender] = useState('');
    const [orientation, setOrientation] = useState('');

  
  
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();
        if (file === null) {

            alert("You failed to enter necessary information")
            return
        } 
    
        formData.append('image', file);
        formData.append('username', username)
        formData.append('email', email)
        formData.append('zipcode', zipcode)
        formData.append('birthday', birthday)
        formData.append('gender', gender)
        formData.append('orientation', orientation)
    
    
        try {
            fetch('/api/register', {
                method: 'POST',
                body: formData,
          })
          .then(r => r.json())
          .then(d => {
            console.log(d)
            setNewUser(d.newUser)
            setUser(d.user)
        })
        } catch (error) {
          console.error('Error occurred during image upload:', error);
        }
      };
    
   
    
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
    };
    
    const handleUsernameChange = (event) => {
        console.log(event.target.value)
        setUsername((username) => event.target.value)
    }
    
    const handleEmailChange = (event) => {
        console.log(event.target.value)
        setEmail((email) => event.target.value)
    }

    const handleZipCodeChange = (event) => {
        console.log(event.target.value)
        setZipcode((zipcode) => event.target.value)
    }
    
    
    
      return (
        <div class="upload-container">
          <img></img>
          <h7 className='pi' >Change Profile Image</h7>
          <input type="file" onChange={handleFileChange} accept="image/*" />
          {file && (
            <div>
              <img className='preview-image' src={ URL.createObjectURL(file)} alt="Selected file" />
            </div>
          )}
            <h7>Username:</h7>
            <input onChange={handleUsernameChange} type="text" value={username} />
            <h7>Birthdate:</h7>
            <input type="date" value={birthday} onChange={e => setBirthday(e.target.value)} />

            <h7>Email:</h7>
            <input onChange={handleEmailChange} type="text" value={email} />
            <label for="gender">Gender:</label>
            <select value={gender} onChange={e=> setGender(e.target.value)} name="gender">
            <option value="">--Please choose an option--</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            </select>   

            <label for="orientation">Orientation:</label>
            <select value={orientation} onChange={e => setOrientation(e.target.value)} name="orientation">
            <option value="">--Please choose an option--</option>
            <option value="Straight">Straight</option>
            <option value="Gay">Gay</option>
            <option value="Other">Other</option>
    
            </select>
          <h7>Zip Code:</h7>
          <input onChange={handleZipCodeChange} type="text" value={zipcode} />
          <button onClick={handleSubmit}>Create Account</button>
        </div>
      );
};

export default NewAccount;