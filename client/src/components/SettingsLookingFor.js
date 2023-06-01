import React, {useState} from 'react';
import '../index.css';
import {Link } from "react-router-dom";
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper } from '@mui/material';

const SettingsLookingFor = ({user, onUpdateAccount}) => {

    const [gender, setGender] = useState(user.interested_in.split('/')[0]);
    const [ethnicity, setEthnicity] = useState(user.interested_in.split('/')[1])
    const [relStatus, setRelStatus] = useState(user.interested_in.split('/')[2])
    const [diet, setDiet]= useState(user.interested_in.split('/')[3])
    const [religion, setReligion] = useState(user.interested_in.split('/')[4])
    const [orientation, setOrientation] = useState(user.interested_in.split('/')[5]);
    const [distance, setDistance] = useState(user.interested_in.split('/')[6]);
    const [ageRange, setAgeRange] = useState(user.interested_in.split('/')[7].split(','));


    const genderOptions = ["Male", 'Female', 'Other']
    const orientationOptions = ['Straight', 'Gay', 'Bisexual', 'Other']
    const ethnicityOptions = ['Black', 'Asian', 'Indian', 'Hispanic', 'Middle Eastern', 'Native American', 'Pacific Islander', 'White', 'Other']
    const relStatusOptions = ['Monogamous', 'Non-Monogamous' ]
    const dietOptions = ['Omnivore', "Vegetarian", "Vegan" ]
    const religionOptions = ["Agnosticism", "Atheism", "Christianity", "Judaism", "Catholicism", "Islam", "Hinduism", "Buddhism", "Sikh", "Other"]
    const distanceOptions =  [5, 10, 15, 25, 50, 100, 500, 1000]
   

  
    console.log(user)
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();
        
        const interestArray = [gender, ethnicity, relStatus, diet, religion, orientation, distance, ageRange] 
        
        const interests = interestArray.join('/')  
       
        formData.append('interested_in', interests)

        onUpdateAccount(formData)
      };
    

    
    
    
      return (
        <div class="settings-container">
            

        <Box marginBottom={2} marginTop={4}>
        <h2>I'm Interested In:</h2>
            <Box marginBottom={4} marginTop={4}>
                <Typography id="range-slider" gutterBottom>
                    Age range
                </Typography>
                <Slider
                    value={ageRange}
                    onChange={(e, newValue) => setAgeRange(()=> newValue)}
                    valueLabelDisplay="auto"
                    aria-labelledby="range-slider"
                    min={18}
                    max={100}
                    name='age'
                    disableSwap
                />
            </Box>
            <Box marginBottom={2}>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 100 }} >
        
                    <InputLabel id="gender-label">Gender</InputLabel>
                    <Select
                        labelId="gender-label"
                        id="gender"
                        value={gender}
                        name='gender'
                        onChange={(e)=> setGender(()=> e.target.value)}
                        label="Gender"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {genderOptions.map(g => (
                            <MenuItem value={g}>
                                {g}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
    
                    <InputLabel id="orientation-label">Orientation</InputLabel>
                    <Select
                        labelId="orientation-label"
                        id="orientation"
                        name='orientation'
                        value={orientation}
                        onChange={(e)=> setOrientation(()=> e.target.value)}
                        label="Orientation"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {orientationOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>
            <Box marginBottom={2}>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
                    <InputLabel id="ethnicity-label">Ethnicity</InputLabel>
                    <Select
                    labelId="ethnicity-label"
                    name="ethnicity"
                    value={ethnicity}
                    onChange={(e)=> setEthnicity(()=> e.target.value)}
                    label="Ethnicity"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {ethnicityOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
                    
                    <InputLabel id="relStatus-label">Status</InputLabel>
                    <Select
                    labelId="relStatus-label"
                    name="status"
                    value={relStatus}
                    onChange={(e)=> setRelStatus(()=>e.target.value)}
                    label="Status"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {relStatusOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>
            <Box marginBottom={2}>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
                    <InputLabel id="diet-label">Diet</InputLabel>
                    <Select
                    labelId="diet-label"
                    name="diet"
                    value={diet}
                    onChange={(e)=> setDiet(()=>e.target.value)}
                    label="Diet"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {dietOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
                    
                    <InputLabel id="religion-label">Religion</InputLabel>
                    <Select
                    labelId="religion-label"
                    name="religion"
                    value={religion}
                    onChange={(e)=> setReligion(()=>e.target.value)}
                    label="Religion"
                    >
                        <MenuItem value="NA">
                            <em>None</em>
                        </MenuItem>
                        {religionOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>
            <Box marginBottom={2}>
                <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
                    <InputLabel id="distance-label">Distance</InputLabel>
                    <Select
                    labelId="distance-label"
                    name="distance"
                    value={distance}
                    onChange={(e)=>setDistance(()=>e.target.value)}
                    label="Distance"
                    >
                        {distanceOptions.map(o => (
                            <MenuItem value={o}>
                                {o}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

            </Box>

        </Box>
        <Box  marginBottom={5}>
        <Button type='submit' onClick={handleSubmit} variant="contained" color="primary">Submit</Button>
        </Box >
{/* 
            <label for="gender">Gender:</label>
            <select value={gender} onChange={e=> setGender(e.target.value)} name="gender">
                <option value="">--Please choose an option--</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="NA">Doesn't Matter</option>
            </select>   


            <label for="ethnicity">Ethnicity:</label>
                <select value={ethnicity} onChange={e => setEthnicity(e.target.value)} name="ethnicity">
                <option value="">--Please choose an option--</option>
                <option value="Black">Black</option>
                <option value="Asian">Asian</option>
                <option value="Indian">Indian</option>
                <option value="Hispanic">Hispanic/Latin</option>
                <option value="Middle Eastern">Middle Eastern</option>
                <option value="Native American">Native American</option>
                <option value="Pacific Islander">Pacific Islander</option>
                <option value="White">White</option>
                <option value="Other">Other</option>
                <option value="NA">Doesn't Matter</option>
            </select>

            <label for="relStatus">Status:</label>
            <select value={relStatus} onChange={e => setRelStatus(e.target.value)} name="relStatus">
                <option value="">--Please choose an option--</option>
                <option value="Monogamous">Monogamous</option>
                <option value="Non-Monogamous">Non-Monogamous</option>
                <option value="NA">Doesn't Matter</option>
                .
            </select>


            <label for="diet">Diet:</label>
            <select value={diet} onChange={e => setDiet(e.target.value)} name="diet">
                <option value="">--Please choose an option--</option>
                <option value="Omnivore">Omnivore</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="NA">Doesn't Matter</option>
            </select>

            <label for="religion">Religion:</label>
            <select value={religion} onChange={e => setReligion(e.target.value)} name="religion">
                <option value="">--Please choose an option--</option>
                <option value="Agnosticism">Agnosticism</option>
                <option value="Atheism">Atheism</option>
                <option value="Christianity">Christianity</option>
                <option value="Judaism">Judaism</option>
                <option value="Catholicism">Catholicism</option>
                <option value="Islam">Islam</option>
                <option value="Hinduism">Hinduism</option>
                <option value="Buddhism">Buddhism</option>
                <option value="Sikh">Sikh</option>
                <option value="Other">Other</option>
                <option value="NA">Doesn't Matter</option>
            </select>
          <button onClick={handleSubmit}>Create Account</button> */}
        </div>
      );
};

export default SettingsLookingFor;