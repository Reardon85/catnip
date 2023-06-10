import React, {useState} from 'react';
import '../index.css';
import {Link } from "react-router-dom";
import LogoutButton from './LogoutButton';

const SettingsBasic = ({user, onUpdateAccount, onDeleteAccount}) => {

    const [email, setEmail] = useState(user.email);
    const [file, setFile] = useState(null);
    const [zipcode, setZipcode] = useState(user.zipcode);
    const [bio, setBio] = useState(user.bio);
    const [hobbies, setHobbies] = useState(user.hobbies)

  
  
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();
        if (file !== null) {
            formData.append('image', file);
        } 
   
        
        formData.append('email', email)
        formData.append('zipcode', zipcode)
        formData.append('bio', bio)
        formData.append('hobbies', hobbies)

        onUpdateAccount(formData)
      };
    
   
    
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
    };
    

    
    
    
      return (
        
        <div class="upload-container">
            
           
          
            <h7 className='pi' >Change Profile Image</h7>
            <input type="file" onChange={handleFileChange} accept="image/*" />
            {file && (
            <div>
                <img className='preview-image' src={ URL.createObjectURL(file)} alt="Selected file" />
            </div>
            )}

            <h7>Email:</h7>
            <input onChange={(e)=> setEmail((email)=> e.target.value)} type="text" value={email} />
            
 
          <h7>Zip Code:</h7>
          <input  onChange={e => setZipcode((zipcode)=> e.target.value)} type="text" value={zipcode} />

            <label>
                Self-Summary
            </label>
            <textarea value={bio} onChange={e => setBio((bio)=> e.target.value)} rows={4} cols={60} maxLength={200}/>

            <label>
                Hobbies
            </label>
            <textarea value={hobbies} onChange={e => setHobbies((hobbies)=> e.target.value)} rows={4} cols={60} maxLength={200}/>


          <button  onClick={handleSubmit}>Update Account</button>
          <button onClick={onDeleteAccount}>Delete Account</button>
          <LogoutButton/>
        </div>
      );
};

export default SettingsBasic;