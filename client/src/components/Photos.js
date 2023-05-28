import React, {useEffect, useState} from 'react';
import './styles/app.css';
import {useParams} from "react-router-dom";
import PhotoCarousel from './PhotoCarousel';
import { Container} from 'react-bootstrap';

const Photos = () => {

    const [photoList, setPhotoList] = useState([])
    const {userId} = useParams()
  
    useEffect(() => {
        //User_Photos - get
        fetch(`/api/user/photos/${userId}`)
            .then((r) => {
                if (!r.ok){
                    r.json().then((err) => {throw new Error(err)});
                }
                return r.json();
            })
            .then((data) => {
                setPhotoList(data);
            })
            .catch((err) => {
                console.log(err);
            })
    }, [userId]);
  
    const handleRemoveImage = (id) => {

        fetch(`/api/photo/${id}`, {
            method: 'DELETE',     
        })
        .then((r) => {
            if (!r.ok){
                r.json().then((err) => {throw new Error(err)})
            }
            return r.json()
        })
        .then((data) => {
            //add code to remove image from array
        })
        .catch((err) =>{
            console.log(err);
        })
    }


    const photoArray = photoList.map((photo, i) => (
        <div className='test'>
            <img alt="" src={photo.image_url} className='user-photo' />
            <p className="legend">photo.description</p>
            <button onClick={() => handleRemoveImage(photo.id)} className="btn btn-danger">Remove</button>
        </div>
    ))

    return (
        <div>
        <Container>
        <PhotoCarousel photoArray={photoArray}/>
        </Container>
        </div>
    );
};

export default Photos;