import React, { useState } from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';


const images = ['https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image3.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image11.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image12.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image2.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image4.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image5.jpg',]




const PhotoCarousel = ({photoArray, setCurrentPhoto}) => {

    

    const getConfigurableProps = () => ({
        showArrows: false,
        showStatus: true,
        showIndicators: true,
        infiniteLoop: true,
        showThumbs: true,
        useKeyboardArrows: true,
        autoPlay: false,
        stopOnHover: true,
        swipeable: false,
        dynamicHeight: false,
        emulateTouch: true,
        autoFocus: false,
        thumbWidth: 80,
        selectedItem: 0, 
        interval: 2000, 
        transitionTime:  500, 
        swipeScrollTolerance:  5, 
        ariaLabel: undefined,
    });


    return (

        <Carousel  {...getConfigurableProps()}  onClickThumb={(number)=>setCurrentPhoto((currentPhoto)=> number)} swipeable={false}>

            {photoArray}
{/* 
        <div className='test'>
            <img alt="" src={images[0]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div>
        <div className='test'>
            <img alt="" src={images[1]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div>
        <div className='test'>
            <img alt="" src={images[2]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div>
        <div className='test'>
            <img alt="" src={images[2]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div>
        <div className='test'>
            <img alt="" src={images[4]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div>
        <div className='test'>
            <img alt="" src={images[4]} className='user-photo' />
            <p className="legend">Legend 1</p>
        </div> */}

       

    </Carousel>
    )
};

export default PhotoCarousel