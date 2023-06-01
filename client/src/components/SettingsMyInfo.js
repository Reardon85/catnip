import React, {useState} from 'react';
import '../index.css';
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper } from '@mui/material';


const SettingsMyInfo = ({user, onUpdateAccount}) => {


    const [gender, setGender] = useState(user.gender);
    const [orientation, setOrientation] = useState(user.orientation);
    const [ethnicity, setEthnicity] = useState(user.ethnicity)
    const [relStatus, setRelStatus] = useState(user.status)
    const [height, setHeight] = useState(user.height)
    const [diet, setDiet]= useState(user.diet)
    const [religion, setReligion] = useState(user.religion)

    const genderOptions = ["Male", 'Female', 'Other']
    const orientationOptions = ['Straight', 'Gay', 'Bisexual', 'Other']
    const ethnicityOptions = ['Black', 'Asian', 'Indian', 'Hispanic', 'Middle Eastern', 'Native American', 'Pacific Islander', 'White', 'Other']
    const relStatusOptions = ['Monogamous', 'Non-Monogamous' ]
    const dietOptions = ['Omnivore', "Vegetarian", "Vegan" ]
    const religionOptions = ["Agnosticism", "Atheism", "Christianity", "Judaism", "Catholicism", "Islam", "Hinduism", "Buddhism", "Sikh", "Other"]
    const heightOptions = []
    
    for (let i=48; i <=84; i++){
        heightOptions.push(i)
    }

  
  
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const formData = new FormData();

    
        formData.append('status', relStatus);
        formData.append('religion', religion)
        formData.append('diet', diet)
        formData.append('ethnicity', ethnicity)
        formData.append('height', height)
        formData.append('gender', gender)
        formData.append('orientation', orientation)

        onUpdateAccount(formData)
      };
    
      
      return (
        <div class="settings-container">
            

        <Box marginBottom={2} marginTop={4}>
        <h2>My Info:</h2>

            <Box marginBottom={2} marginTop={6}>
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
        
                    <InputLabel id="distance-label">Height</InputLabel>
                    <Select
                    labelId="distance-label"
                    name="height"
                    value={height}
                    onChange={(e)=>setHeight(()=>e.target.value)}
                    label="Height"
                    >
                        {heightOptions.map(o => (
                            <MenuItem value={o}>
                                {`${Math.floor(o/12)}' ${o%12}"`}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

            </Box>

        </Box>
        <Box  marginBottom={5}>
        <Button type='submit' onClick={handleSubmit} variant="contained" color="primary">Submit</Button>
        </Box >
        </div>
      );
};

export default SettingsMyInfo;