#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker
from uuid import uuid4
import time

# Local imports
from app import app, add_coordinates
from config import app, db
from models import Visitor, Message, User, Conversation, Match, Photo, Pet, PetPhoto, favorites, datetime, timedelta


fake = Faker()

zip_codes = ['43201', '43202', '43203', '43204', '43205', '43206', '43207', '43209', '43210', '43211', '43212', '43213', '43214', '43215', 
             '43216', '43217', '43218', '43219', '43220', '43221', '43222', '43223', '43224', '43226', '43227', '43228', '43230', 
             '43231', '43232', '43234', '43235', '43236', '43240', '43251', '43260', '43266', '43268', '43270', '43271', '43272', '43279', 
             '43287', '43291', '45402', '45409', '44113', '44115', '19103',  '10001', '10002', '60601', '60602', '30303', 
             '30309', '90001', '90002', '98101', '98102', "78701", "78702", "75201", "75202", "75201", "75202"]

bio_info = [
    "I'm a Funny Scientist",
    "I'm a Dumb Cat Lover",
    "I Don't Know How To Read!!! LULZ",
    "I Died 12 Years Ago and my Soul Got Stuck On This Site....",
    "I'm an Animal Lover who loves to Bike.",
    "I Use to Own an Airplane",
    "My Friends Call me Biz.",
    "I'm a very sad person.....",
    "Where did all the Cowboy's go?",
    "Does anyone Remember the movie the Matrix?",
    "I use to be a Professional Cowboy",
    "If you Follow me I'll Follow You Back!!!"
]
female_pic = [
    'https://the-tea.s3.us-east-2.amazonaws.com/profile1.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile11.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile12.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile13.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile14.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile15.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile2.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile20.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile21.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile22.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile28.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile3.webp',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile3.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile31.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile4.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile5.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile6.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile9.jpg',
    'https://images.unsplash.com/photo-1464863979621-258859e62245?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2572&q=80',
    'https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1499557354967-2b2d8910bcca?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1336&q=80',
    'https://images.unsplash.com/photo-1508184964240-ee96bb9677a7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1532074205216-d0e1f4b87368?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=882&q=80',
    'https://images.unsplash.com/photo-1532549453886-602b1eeda04e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1603074396433-1d3359139e94?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1604613444463-696165f2de00?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=928&q=80',
    'https://images.unsplash.com/photo-1492106087820-71f1a00d2b11?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1509967419530-da38b4704bc6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1195&q=80',
    'https://images.unsplash.com/photo-1506956191951-7a88da4435e5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1374&q=80',
    'https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1529218164294-0d21b06ea831?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80',
    'https://images.unsplash.com/photo-1491234710240-3113bbcc62c9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1519699047748-de8e457a634e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1180&q=80',
    'https://images.unsplash.com/photo-1541823709867-1b206113eafd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1526835746352-0b9da4054862?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1632387861274-fe4bbdeb28be?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1619817278902-42bd23925bf6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1519011985187-444d62641929?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=928&q=80',
    'https://images.unsplash.com/photo-1526382925646-27b5eb86796e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1180&q=80',
    'https://images.unsplash.com/photo-1678696395436-d8309f157359?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1597586124394-fbd6ef244026?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1681500920181-0aff411f8cab?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1156&q=80',
    'https://images.unsplash.com/photo-1589911949435-718743b6032c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1554128408-d2ae7deb38ee?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1632387861274-fe4bbdeb28be?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1530047198515-516ff90fc4d9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1550456915-749f38312cbe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1565325058830-96445e1dd4b2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1617835215490-89dd69d0ec2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1634746715098-6cafbc6a7a00?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1617383619206-e88d5848bacc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=854&q=80',
    'https://images.unsplash.com/photo-1583345784606-9f59c99488de?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80',
    'https://images.unsplash.com/photo-1570751057249-92751f496ee3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1521610142770-4f09a2cdb252?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1612913736760-fd187fec8500?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'
]

male_pic= [
    'https://the-tea.s3.us-east-2.amazonaws.com/profile10.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile16.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile18.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile17.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile19.jpeg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile23.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile24.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile25.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile26.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile27.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile29.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile7.jpg',
    'https://the-tea.s3.us-east-2.amazonaws.com/profile8.jpg',
    'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1590086782792-42dd2350140d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://plus.unsplash.com/premium_photo-1671656349322-41de944d259b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1531384441138-2736e62e0919?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1525457136159-8878648a7ad0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1596075780750-81249df16d19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://plus.unsplash.com/premium_photo-1675129779575-54b713ec81dc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1527082395-e939b847da0d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80',
    'https://images.unsplash.com/photo-1530983822321-fcac2d3c0f06?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1134&q=80',
    'https://plus.unsplash.com/premium_photo-1675129522693-bd62ffe5e015?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1590086782957-93c06ef21604?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1596502059330-be10388e3ba0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80',
    'https://images.unsplash.com/photo-1523111523695-543da7cd722c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=627&q=80',
    'https://images.unsplash.com/photo-1627686011747-74adda3d2343?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1514278033938-06f80809a42c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
    'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1148&q=80',
    'https://images.unsplash.com/photo-1618673827854-0065d21af001?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=627&q=80',
    'https://images.unsplash.com/photo-1565884280295-98eb83e41c65?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1440133197387-5a6020d5ace2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80',
    'https://images.unsplash.com/photo-1530505580493-3fa88046af67?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'
]
profile_pic = [








]

content_list= [
    "Check out this Photo",
    "I took this when I was traveling",
    "This was so much fun",
    "You Know I'm gonna spill that tea",
    "Best day ever!",
    "I only wish that you guys could have seen it!",
    "Just living my best life!",
    "Feeling blessed and grateful today.",
    "Exploring new places and making memories.",
    "Sometimes the best therapy is a long drive and good music.",
    "Life is short, enjoy the little things.",
    "Creating moments that will last a lifetime.",
    "Happiness is a journey, not a destination.",
    "Life's too short to not take risks.",
    "Embracing the chaos and loving every minute of it.",
    "Dream big, work hard, stay focused, and surround yourself with good people.",
    "The only limit is the one you set for yourself.",
    "Always trust the journey, even if you don't understand it.",
    "Life is an adventure, embrace it with open arms.",
    "You are the artist of your own life, don't be afraid to paint outside the lines.",
    "Every day is a new opportunity to grow and learn.",
    "Make every moment count, and never forget to smile.",
    "Be the reason someone smiles today.",
    "Believe in yourself and all that you are.",
    "Chase your dreams and never look back.",
    "Love yourself, embrace your flaws, and never stop being you."
]

post_pic = [
'https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image11.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image12.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image2.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image3.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image4.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image5.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image6.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image7.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image8.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image9.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img13.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img14.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img15.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img16.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img17.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img18.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img19.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img20.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img21.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img22.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img23.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img24.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img25.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img26.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img27.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img29.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img30.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img31.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img32.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img33.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img34.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img35.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img36.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img37.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img38.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img39.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img40.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img41.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img42.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img43.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img44.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img45.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img46.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img47.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img48.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img49.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img50.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img51.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img52.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img53.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img54.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img55.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img56.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img57.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img58.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img59.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img60.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img61.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img62.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img63.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img64.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img65.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img66.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img67.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img68.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img69.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img70.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img71.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img72.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img73.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img74.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img75.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img76.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img77.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img78.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img79.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img80.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img81.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img82.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img83.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img84.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img85.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img86.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img87.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img88.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img89.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img90.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img91.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img92.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img93.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img94.jpg',
]


# 'https://the-tea.s3.us-east-2.amazonaws.com/emb1.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb2.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb3.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb4.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb5.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb6.png',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk1.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk10.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk11.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk12.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk13.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk14.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk15.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk16.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk17.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk19.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk2.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk21.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk22.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk23.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk24.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk25.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk26.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk27.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk28.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk29.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk3.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk30.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk31.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk32.webp'
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk33.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk4.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk5.jpeg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk6.jpeg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk7.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk8.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk9.jpg'


nice_comments = [
'So beautiful! 😍',
'Love this angle! 👌',
'This is giving me all the feels! ❤️',
'Wow, stunning photo! 📸',
"You're killing it, girl! 🔥",
'Goals! 💪',
'This looks like so much fun!',
'Where is this? I need to go there! 🌴',
'That made me smile! 😊',
'Obsessed with this look!',
'So jealous, wish I was there! 😩',
'Incredible shot! 🤩',
'You are a true inspiration! 💫',
'I need this in my life!',
'Can I borrow this image? 😉',
'This makes me want to book a flight ASAP! ✈️',
'Gorgeous as always! 💕',
'This is the definition of vacation goals! 🏖️',
"You're living your best life! 👏",
"I can't get enough of this picture!", 

]

bad_comments = [
"This is hilarious!",
"I can't stop laughing at this! 🤣",
"This made my day! 😆",
"I'm crying laughing! 😭",
"You always know how to make me laugh!",
"I needed this laugh, thank you!",
"How do you come up with this stuff?!", 
"You're too funny! 😂",
"I just snorted my drink!", 
"I can't breathe, this is too funny!",
"I'm sharing this with all my friends! 😂",
"You win the internet today! 🏆",
"This is the best thing I've seen all week!",
"My sides hurt from laughing so hard!",
"You're a comedic genius!",
"I'm going to be laughing about this all day!",
"This is the type of content I live for! 😂",
"You're officially my favorite Tea account!",
"I'm sending this to everyone I know!",
"You deserve an award for this post!",

]

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        db.session.query(favorites).delete()
        PetPhoto.query.delete()
        Match.query.delete()
        Photo.query.delete()
        Pet.query.delete()
        Visitor.query.delete()
        Message.query.delete()
        Conversation.query.delete()
        User.query.delete()
        db.session.commit()


        print('Creating User objects...')


        genderOptions = ["Male", 'Female', "Male", 'Female', "Male", 'Female', 'Other']
        orientationOptions = ['Straight', 'Straight', 'Straight', 'Straight', 'Straight', 'Straight', 'Straight',   'Gay', 'Bisexual', 'Gay', 'Bisexual' 'Other']
        ethnicityOptions = ['Black', 'Asian', 'Indian', 'Hispanic', 'Middle Eastern', 'Native American', 'Pacific Islander', 'White', 'Other']
        relStatusOptions = ['Monogamous', 'Monogamous', 'Monogamous', 'Non-Monogamous' ]
        dietOptions = ['Omnivore', 'Omnivore', 'Omnivore', "Vegetarian", "Vegan" ]
        religionOptions = ["Agnosticism", "Atheism", "Christianity", "Judaism", "Catholicism", "Islam", "Hinduism", "Buddhism", "Sikh", "Other"]
        self_summaries = [
        "Adventurous foodie, loves exploring new cuisines.",
        "Jazz lover and amateur pianist. Let's make music together.",
        "Vegan yogi who loves nature and animals.",
        "Avid hiker and amateur photographer. Let's capture moments.",
        "Fitness enthusiast with a passion for cooking healthy meals.",
        "Software engineer who enjoys board games and coding.",
        "Film buff and writer, inspired by the classics.",
        "Animal lover and volunteer at local animal shelters.",
        "Bibliophile and coffee addict, always up for a good chat.",
        "Surfer and ocean lover, happiest near the sea.",
        "Traveler with a long bucket list. Let's explore together.",
        "Passionate about sustainable living and organic farming.",
        "Aspiring novelist and part-time poet.",
        "Tea connoisseur with a penchant for cozy mysteries.",
        "Art lover and painter, inspired by the Impressionists.",
        "Baker who can whip up a mean chocolate chip cookie.",
        "Plant mom with a green thumb and a love for gardening.",
        "Aspiring chef with a flair for Italian cuisine.",
        "Dancer and fitness enthusiast, loves Zumba.",
        "Guitarist in a local band, loves live music.",
        "Astronomy enthusiast, loves stargazing on clear nights.",
        "Bird watcher and nature lover.",
        "Skiing enthusiast, loves the thrill of the slopes.",
        "DIY-er and woodworker, loves creating things with my hands.",
        "History buff, fascinated by medieval history.",
        "Amateur astronomer with a telescope at the ready.",
        "Vintage car enthusiast, always ready for a road trip.",
        "Biology teacher with a love for marine life.",
        "Architect with a passion for sustainable design.",
        "Self-proclaimed tech geek and video game aficionado.",
        "Stargazer with a love for the mysteries of the universe.",
        "Nurse with a caring heart and a passion for helping others.",
        "Amateur chef who loves to experiment with flavors.",
        "Professional pastry chef with a sweet tooth.",
        "Coffee lover with a taste for adventure.",
        "Dog lover with a soft spot for golden retrievers.",
        "Cat lover, happiest with a book and a cup of tea.",
        "Engineer with a passion for robotics.",
        "Math teacher who loves puzzles and brain teasers.",
        "Avid runner training for my first marathon.",
        "Cyclist who loves exploring the city on two wheels.",
        "Fashionista with a love for vintage clothes.",
        "Scientist with a fascination for the cosmos.",
        "Weekend warrior, loves camping and hiking.",
        "Wine connoisseur with a taste for travel.",
        "Art historian with a love for Renaissance paintings.",
        "Archaeologist with a passion for ancient civilizations.",
        "Beer brewer who enjoys trying new recipes.",
        "Physicist with a passion for quantum mechanics.",
        "Musician who loves jazz and blues."
        ]
        Hobbies = [
            "Avid knitter, love the quiet companionship of my old cat, Whiskers.",
            "Proud dog dad who loves long walks with my Labrador, Bella. She's my sunshine!",
            "Pet parent to two rabbits, love their curiosity. Enjoy sketching in my free time.",
            "Love biking and the joyous energy of my border collie, Buddy.",
            "Passionate about bird watching, love my pet bird Kiwi's melodious tunes.",
            "Traveling is my hobby, but coming home to my cat, Muffin, is the best part.",
            "Adventurous rock climber, love the steadfast companionship of my turtle, Rocky.",
            "Photography enthusiast. My Dachshund, Slinky, is my favorite model.",
            "Love cooking gourmet meals, and my cat, Cookie, loves being my taste-tester.",
            "Pottery lover who enjoys the playful antics of my ferret, Noodle.",
            "Hiking enthusiast, my dog, Scout, is the best trail buddy.",
            "Chess player who appreciates my cat, Checkers, for her strategic napping spots.",
            "Painter with a love for my dog, Picasso, who’s my loyal studio buddy.",
            "Gardening lover, my rabbit, Daisy, loves our veggie patch as much as I do.",
            "Homebrewer who loves sharing my couch with my bulldog, Stout.",
            "Stargazer with a cat, Orion, who loves night-time cuddles.",
            "Fitness enthusiast, love how my husky, Storm, keeps me on my toes.",
            "Novelist with a pet owl, Quill, who's my night-time writing companion.",
            "Scuba diver who loves the playful energy of my otter, Bubbles.",
            "Classical musician with a cat, Mozart, who purrs along to my violin.",
            "Love baking and sharing my creations with my hungry Labrador, Donut.",
            "Skier with a St. Bernard, Snowball, who loves the winter as much as I do.",
            "Astronomy enthusiast with a star-loving cat, Galaxy.",
            "Antique collector who loves the patient companionship of my tortoise, Timer.",
            "Movie buff with a Corgi, Popcorn, who's my cuddle buddy during movie nights.",
            "Crossword lover with a cat, Puzzles, who loves to help by sitting on them.",
            "Woodworker with a loyal golden retriever, Chip, who’s always by my side.",
            "Runner with a greyhound, Bolt, who keeps me fit and happy.",
            "Love fishing and the laid-back attitude of my cat, Bobber.",
            "Bibliophile who loves reading with my tabby, Page, on my lap.",
            "Volunteer at a shelter, love the endless affection of my rescue dog, Hero.",
            "Mountain biker with a Boxer, Trail, who loves the outdoors as much as I do.",
            "Baker who loves the enthusiastic taste-testing of my Beagle, Biscuit.",
            "Swimmer with a water-loving Labrador, Splash.",
            "Camping enthusiast with a Border Collie, Campfire, who's my adventure partner.",
            "Nature photographer who loves the curious nature of my ferret, Snap.",
            "Yoga practitioner with a cat, Zen, who has the best downward dog pose.",
            "Chef who loves the culinary curiosity of my cat, Gourmet.",
            "Birdwatcher with a Cockatoo, Echo, who loves mimicking"
        ]

        male_usernames = [
    "AdventureSteve", "PoeticPaul", "FitFrank", "TravelingTom", "GourmetGreg",
    "ArtisticAlan", "CharmingChris", "ActiveAndrew", "MusicalMike", "HandyHarry",
    "GamingGary", "SportySam", "OutdoorsyOliver", "NatureNick", "RomanticRob",
    "JazzJake", "BookwormBrian", "DogLoverDan", "EnergeticEthan", "ComedyCarl",
    "FishingFred", "TechieTodd", "BikingBen", "SailingSean", "PhotographyPhil",
    "GuitaristGeorge", "BakingBill", "CraftyClint", "HikingHenry", "CampingCaleb",
    "DancingDave", "RunningRalph", "GardeningGabriel", "WriterWill", "CookingCody",
    "MovieManMark", "FashionForwardFelix", "WorkoutWarren", "VolunteerVince", "YogaYuri",
    "BaseballBob", "MagicMatt", "QuirkyQuentin", "LoyalLuke", "FoodieFinn",
    "QuietQuinn", "RowdyRex", "ZestyZack", "UnderwaterUli", "XtraordinaryXander",
    "YachtingYves", "ZealousZane", "VivaciousVinny", "UnstoppableUlysses", "TrailblazingTrevor",
    "SpiritedScott", "RadiantRussell", "QuixoticQuincy", "PersistentPete", "ObservantOscar",
    "NurturingNathan", "MindfulMason", "LovingLance", "KindheartedKai", "JoyfulJerry",
    "InquisitiveIan", "HumorousHugo", "GenerousGideon", "FriendlyFloyd", "EncouragingEvan",
    "DevotedDerek", "CaringCooper", "BenevolentBrent", "AffectionateArnie", "AdventurousAce",
    "AstroAdam", "BluesBobby", "CinephileCasey", "DreamyDylan", "ExplorerEli",
    "FoodLoverFergus", "GeekyGraham", "HipHopHank", "IndieIgor", "JoggingJasper",
    "KnightlyKurt", "LiteraryLiam", "MangaMarty", "NerdNigel", "OperaticOrson",
    "PunkPeter", "QuirkyQuestor", "RockNRollRonnie", "SciFiSid", "ThrillerTheo",
    "UrbanUpton", "VintageVal", "WackyWarwick", "XMenXavier", "YogiYancey", "ZanyZeb",
    "FidoLover", "KittyWhiskers", "ParrotTalker", "BunnyHugger", "GoldFishDreamer",
    "HamsterWheel", "DoggieDoodler", "BirdWatcher", "PawsAndClaws", "FeathersAndScales",
    "LabradorFan", "BulldogBestie", "RetrieverRaver", "PersianPurrer", "SiameseSmiler",
    "AquariumAce", "TurtleTrotter", "PythonPal", "LizardLover", "HuskyHero",
    "ShepherdStar", "TabbyTeaser", "SphynxSinger", "RagdollRambler", "MaineCoonMuse",
    "PomeranianPioneer", "BichonBuddy", "DachshundDancer", "PoodlePartner", "PugPatriot",
    "CorgiCrafter", "RottweilerRider", "YorkieYodeler", "MalteseMaestro", "BoxerBouncer",
    "ChihuahuaChampion", "BeagleBeliever", "ShihTzuShaman", "BulldogBard", "TerrierTinkerer",
    "SiberianHuskyHugger", "GreatDaneGazer", "DobermanDoter", "BernardBouncer", "PomeranianPrince",
    "PoodlePrincess", "RagdollRascal", "MaineCoonMagician", "PersianPrankster", "SiameseSorcerer",
    "CalicoCaper", "TabbyTroublemaker", "SphynxSpellcaster", "BengalBuccaneer", "RottweilerRogue",
    "BeagleBard", "YorkieYeoman", "DachshundDuke", "ShihTzuSheriff", "ChihuahuaChieftain",
    "BoxerBaron", "PomeranianPaladin", "PugPirate", "CorgiConqueror", "PoodlePeasant",
    "HuskyHarlequin", "LabradorLad", "RetrieverRake", "BulldogBohemian", "TerrierThespian",
    "RagdollRanger", "MaineCoonMercenary", "PersianPilgrim", "SiameseSettler", "BengalBandit",
    "CalicoColonist", "TabbyTrader", "SphynxSurveyor", "GoldfishGoldminer", "TurtleTrader",
    "ParrotPioneer", "KittenKnight", "PuppyPrince", "HamsterHermit", "BunnyBaron",
    "DoveDuchess", "FerretFarmer", "GuineaPigGardener", "IguanaInventor", "ParakeetPainter",
    "RabbitRider", "CanaryComposer", "FinchFarmer", "LionLover", "TigerTamer",
    "ElephantEnthusiast", "KoalaKeeper", "PandaPatron", "KangarooKing", "ArmadilloAdmirer",
    "ButterflyBuddy", "BeetleBestie", "CaterpillarCompanion", "DolphinDancer", "GiraffeG"
]

        female_usernames = [
    "ArtsyAnna", "BakingBetty", "CuteCindy", "DancingDiana", "EnergeticEva",
    "FashionFiona", "GardeningGrace", "HikingHannah", "IngeniousIvy", "JazzyJenna",
    "KindheartedKate", "LovingLaura", "MusicalMelinda", "NatureNina", "OptimisticOlga",
    "PassionatePam", "QuirkyQuinn", "ReadingRachel", "SportySara", "TravelingTina",
    "UniqueUrsula", "VivaciousVicky", "WittyWendy", "eXcitingXena", "YogaYvonne",
    "ZestyZara", "AdventurousAlice", "BookwormBella", "CreativeCora", "DogLoverDaisy",
    "EcoFriendlyEmma", "FitFelicity", "GourmetGina", "HandyHaley", "IntellectualIsabella",
    "JoggingJulia", "KnittingKylie", "LiteraryLily", "MindfulMegan", "NurturingNicole",
    "OutdoorOphelia", "PhotographyPiper", "QuietQueenie", "RomanticRiley", "SewingSophie",
    "TechieTara", "UnstoppableUma", "VolunteeringVera", "WritingWhitney", "YachtingYasmin",
    "ZenZoe", "AthleticAmy", "BubblyBianca", "CalmCarmen", "DreamyDana", "ExplorerEvelyn",
    "FunFrida", "GenerousGwen", "HumorousHolly", "InspirationalIris", "JoyfulJune",
    "KeenKendra", "LoyalLinda", "MindfulMonica", "NatureLovingNancy", "OptimistOlive",
    "PlayfulPolly", "QuestioningQueen", "RelaxedRosa", "SweetSally", "ThriftyTheresa",
    "UnderstandingUla", "VersatileViolet", "WiseWanda", "eXtraordinaryXara", "YouthfulYana",
    "ZenithZelda", "ActiveAddison", "BraveBridget", "CaringCassie", "DevotedDeanna",
    "EnthusiasticElena", "FriendlyFern", "GentleGemma", "HelpfulHeidi", "IdealisticIsla",
    "JollyJess", "KindKelsey", "LovingLucy", "MotivatedMandy", "NobleNellie",
    "OpenheartedOdette", "PeacefulPenny", "QuietQuincy", "ResilientRoxanne", "SincereSylvia",
    "TruthfulTrudy", "UnderstandingUna", "ValiantValerie", "WarmheartedWinnie", "eXpressiveXylia",
    "YoungAtHeartYvette", "ZanyZinnia",    "FerretFiesta", "LeopardLover", "MouseMaestro", "NightingaleNurturer", "OwlObserver",
    "ParrotPartisan", "QuokkaQueen", "RaccoonRacer", "SquirrelSupporter", "TortoiseTreasurer",
    "UakariUnderstudy", "VoleVirtuoso", "WalrusWarrior", "XerusXenophile", "YakYodeler",
    "ZebraZealot", "AlpacaAdorer", "ButterflyBuddy", "CricketCrafter", "DingoDancer",
    "EagleEnthusiast", "FalconFollower", "GuppyGuru", "HippopotamusHugger", "IguanaIdol",
    "JellyfishJester", "KoalaKnight", "LemurLover", "MeerkatMagician", "NarwhalNovelist",
    "OtterOracle", "PenguinPoet", "QuailQuester", "RabbitRaconteur", "SalamanderScribe",
    "TigerTutor", "UmbrellabirdUsher", "VultureVoyager", "WeaselWizard", "X-rayFishXenogloss",
    "YabbyYogaMaster", "ZonkeyZumbaEnthusiast"
]

        interestOption=[]
        users = []
        matches = []
        first_photo=[]

        users = User.query.all()

        for user in users:
            user.interested_in=f'{rc(genderOptions)}/{rc(ethnicityOptions)}/{rc(relStatusOptions)}/{rc(dietOptions)}/{rc(religionOptions)}/{rc(orientationOptions)}/{25}/{18,35}'


        m_index=0
        f_index=0

        for i in range(200):
            gender = rc(genderOptions)
            if gender == "Male":
                pic= rc(male_pic)
                username = male_usernames[m_index]
                m_index = m_index +1
            elif gender == 'Female':
                pic=rc(female_pic)
                username= female_usernames[f_index]
                f_index = f_index +1
            else:
                pic =rc(female_pic)
                username = male_usernames[m_index]
                m_index = m_index +1
            
            avatar_pic =pic 
            user = User(
                email=fake.email(),
                username= username,
                avatar_url=avatar_pic,
                bio= rc(self_summaries),
                auth_sub= str(uuid4()),
                gender=gender,
                orientation=rc(orientationOptions),
                ethnicity=rc(ethnicityOptions),
                status=rc(relStatusOptions),
                diet=rc(dietOptions),
                religion=rc(religionOptions),
                hobbies=rc(Hobbies),
                height=randint(59,78),
                birthdate=fake.date_time_between(start_date="-30y", end_date="-19y"),
                last_request= datetime.utcnow() - timedelta(days=randint(1,90)),                
                interested_in=f'{rc(genderOptions)}/{rc(ethnicityOptions)}/{rc(relStatusOptions)}/{rc(dietOptions)}/{rc(religionOptions)}/{rc(orientationOptions)}/{25}/{18,35}'
            )
            time.sleep(0.5)
            add_coordinates(rc(zip_codes), user)
            photo = Photo(
                user_id=user.id,
                image_url=avatar_pic,
                description='My Profile Pic'
            )
            first_photo.append(photo)
            users.append(user)




        print('Adding User objects to transaction...')
        db.session.add_all(first_photo)
        db.session.commit()
        print('Committing transaction...') 

        print('Complete.')

        print("Having Each User make 5 posts")
        start = users[0].id + len(users)
        for user in users:
            if user.id < start -7:
                for i in range(5):
                    match = Match(
                        user_one_id = user.id,
                        user_two_id = user.id+i+1,
                        user_one_liked= True,
                        user_two_liked= True,
                    )
                    matches.append(match)

        print('Adding Post objects to transaction...')
        
        db.session.add_all(matches)
        print('Committing transaction...') 
        db.session.commit() 
        print('Complete.')

        print("Creating 5,000 randomly assigned Likes")







        photos = []

        users_list = list(users)


        for user in users_list:
            
            for i in range(5):
                print(i)
                photo = Photo(
                    user_id= user.id,
                    image_url=rc(post_pic),
                    description=rc(content_list)
                )

                db.session.add(photo)



        print('Adding Like objects to transaction...')
        print('Committing transaction...') 
        db.session.commit() 
        print('Complete.')

    

        

