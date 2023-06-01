import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {useSearchParams}  from "react-router-dom";
import SearchResults from './SearchResults.js';
import { CssBaseline } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import {  Select, MenuItem, FormControl, InputLabel, Box, Button, Slider, Typography, Paper } from '@mui/material';

const Search = () => {
    const [searchValue, setSearchValue] = useState({
        age: [18, 80],
        gender: '',
        orientation: '',
        ethnicity: '',
        status:'',
        diet:'',
        religion:'',
        distance: 25,
        sort: ''
    })
    const [searchResults, setSearchResultls] = useState([])
    const[searchParams, setSearchParams] = useSearchParams()
    
    const genderOptions = ["Male", 'Female', 'Other']
    const orientationOptions = ['Straight', 'Gay', 'Bisexual', 'Other']
    const ethnicityOptions = ['Black', 'Asian', 'Indian', 'Hispanic', 'Middle Eastern', 'Native American', 'Pacific Islander', 'White', 'Other']
    const relStatusOptions = ['Monogamous', 'Non-Monogamous' ]
    const dietOptions = ['Omnivore', "Vegetarian", "Vegan" ]
    const religionOptions = ["Agnosticism", "Atheism", "Christianity", "Judaism", "Catholicism", "Islam", "Hinduism", "Buddhism", "Sikh", "Other"]
    const distanceOptions =  [5, 10, 15, 25, 50, 100, 500, 1000]
    const sortOptions = [{label:'Distance', value:'distance' }, {label:'Age', value:'age'},{label :'Last Online', value:'last_request'}, {value:'match_percentage', label:"Compatability"}]

    useEffect(()=> {

        if(searchParams.size > 0){
            fetch(`/api/search/?${searchParams.toString()}`)
            .then(r => {
                if(!r.ok){
                    throw new Error(r.statusText)   
                }
                return r.json()
            })
            .then(data => setSearchResultls(()=> data))
        }


    },[searchParams])



    function valuetext(value) {
        return `${value} years old`;
    }
      
      
    
    
    const handleSubmit = (event) => {
        event.preventDefault()

        const paramsDict={}
        for (let key in searchValue){
            if (searchValue[key] !== 'NA' && searchValue[key] !== ''){
                paramsDict[key] = searchValue[key]
            }
        }
        const params = new URLSearchParams(paramsDict).toString()
        setSearchParams((searchParams)=> params)
    

        fetch(`api/search/?${params}`)
        .then(r => {
            if(!r.ok){
                throw new Error(r.statusText)
            }
            return r.json()
        })
        .then(data => setSearchResultls(data))
        .catch((err)=> console.log(err))
    };

    console.log(searchValue)
    const handleChange = (e, newValue) =>{
        
        if(e.target.name === 'age'){
            setSearchValue((searchValue) =>{
                return {
                    ...searchValue,
                    age: newValue
                }
            }
            )

        }else{
            setSearchValue((searchValue) => {
                return {
                ...searchValue,
                [e.target.name]: e.target.value

            }})
        }
        
    }






//   {[...Array(83).keys()].map(i => (
//     <MenuItem value={i + 18}>{i + 18}</MenuItem>
//   ))}



  return (
    <div style={{width: '100%', margin: '0 auto'}}>
    <Paper elevation={10} >
    <Box marginBottom={2}>
        <Box marginX={50}>
        <Typography id="range-slider" gutterBottom>
            Age range
        </Typography>
        <Slider
            value={searchValue.age}
            onChange={handleChange}
            valueLabelDisplay="auto"
            aria-labelledby="range-slider"
            getAriaValueText={valuetext}
            min={18}
            max={100}
            name='age'
            disableSwap
        />
        </Box>

    <FormControl variant="outlined" sx={{ m: 1, minWidth: 100 }} >
        
            <InputLabel id="gender-label">Gender</InputLabel>
            <Select
            labelId="gender-label"
            id="gender"
            value={searchValue.gender}
            name='gender'
            onChange={handleChange}
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
        value={searchValue.orientation}
        onChange={handleChange}
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
    <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
        <InputLabel id="ethnicity-label">Ethnicity</InputLabel>
        <Select
        labelId="ethnicity-label"
        name="ethnicity"
        value={searchValue.ethnicity}
        onChange={handleChange}
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
        value={searchValue.status}
        onChange={handleChange}
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
    <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
        <InputLabel id="diet-label">Diet</InputLabel>
        <Select
        labelId="diet-label"
        name="diet"
        value={searchValue.diet}
        onChange={handleChange}
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
        value={searchValue.religion}
        onChange={handleChange}
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
    <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
        <InputLabel id="distance-label">Distance</InputLabel>
        <Select
        labelId="distance-label"
        name="distance"
        value={searchValue.distance}
        onChange={handleChange}
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
    <Box marginBottom={2}>
    <FormControl variant="outlined" sx={{ m: 1, minWidth: 150 }} >
        
        <InputLabel id="sort-label">Sort By</InputLabel>
        <Select
        labelId="sort-label"
        name="sort"
        value={searchValue.sort}
        onChange={handleChange}
        label="Sort By"
        >
            {sortOptions.map(o => (
                
                <MenuItem value={o.value}>
                    
                    {o.label}
                </MenuItem>
            ))}
        </Select>
    </FormControl>
    </Box>
    </Paper>
  
        <Box  marginBottom={5}>
        <Button type='submit' onClick={handleSubmit} variant="contained" color="primary">Submit</Button>
        </Box >
        <Box  marginBottom={8}>
        <SearchResults searchResults={searchResults} />
        </Box>
    </div>

    );
};

export default Search;