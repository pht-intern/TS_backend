"""
City to Localities/Areas Mapping
This file contains a comprehensive mapping of cities to their localities/areas.
This data can be used as a fallback or primary source for locality dropdowns.
"""

# Mapping of cities to their localities/areas
CITY_LOCALITIES = {
    # Karnataka
    'Bengaluru': [
        'Whitefield', 'Marathahalli', 'Electronic City', 'HSR Layout', 'Koramangala',
        'Indiranagar', 'Jayanagar', 'JP Nagar', 'BTM Layout', 'Bannerghatta Road',
        'Hebbal', 'Yelahanka', 'Yeshwanthpur', 'Malleswaram', 'Rajajinagar',
        'Vijayanagar', 'Basavanagudi', 'Banashankari', 'Uttarahalli', 'Jalahalli',
        'Peenya', 'Nagarbhavi', 'Vidyaranyapura', 'RT Nagar', 'Frazer Town',
        'Cox Town', 'Shivajinagar', 'MG Road', 'Brigade Road', 'Commercial Street',
        'Richmond Town', 'Lavelle Road', 'Cunningham Road', 'Race Course Road',
        'Domlur', 'Old Airport Road', 'Murugeshpalya', 'Kadubeesanahalli', 'Bellandur',
        'Sarjapur Road', 'Outer Ring Road', 'KR Puram', 'Mahadevapura', 'CV Raman Nagar',
        'Ramamurthy Nagar', 'Kaggadasapura', 'Banaswadi', 'Kalyan Nagar', 'HRBR Layout',
        'Hennur', 'Thanisandra', 'Nagavara', 'Hebbal Kempapura', 'Gunjur',
        'Varthur', 'Panathur', 'Kadugodi', 'Hoodi', 'ITPL', 'Whitefield Main Road'
    ],
    'Mysuru': [
        'Vijayanagar', 'Kuvempunagar', 'Gokulam', 'Nazarbad', 'Saraswathipuram',
        'Vishweshwarapuram', 'Yadavagiri', 'T K Layout', 'Bannimantap', 'Hunsur Road',
        'Bogadi', 'Hinkal', 'Kuvempunagar Extension', 'JP Nagar', 'Vontikoppal',
        'Lakshmipuram', 'Krishnamurthypuram', 'Mandi Mohalla', 'Devaraja Market',
        'Chamarajapuram', 'Ashokapuram', 'Siddharthanagar', 'Vijayanagar 1st Stage',
        'Vijayanagar 2nd Stage', 'Vijayanagar 3rd Stage', 'Vijayanagar 4th Stage'
    ],
    'Mangaluru': [
        'Kadri', 'Bejai', 'Pandeshwar', 'Hampankatta', 'Kankanady',
        'Bendoor', 'Falnir', 'Kodialbail', 'Bolar', 'Urwa',
        'Kulur', 'Padil', 'Bondel', 'Kottara', 'Jeppu',
        'Kadri Park', 'Light House Hill', 'Pumpwell', 'Kankanady', 'Attavar'
    ],
    'Hubballi': [
        'Vidyanagar', 'Gokul Road', 'Deshpande Nagar', 'Keshwapur', 'Hubballi City',
        'Old Hubballi', 'New Hubballi', 'Unkal', 'Bengeri', 'Dharwad Road',
        'Airport Road', 'Gandhi Nagar', 'Keshwapur Extension', 'Keshwapur Main',
        'Vidyanagar Extension', 'Gokul Road Extension'
    ],
    'Belagavi': [
        'Camp', 'Khanapur Road', 'Tilakwadi', 'Shahapur', 'Fort Area',
        'College Road', 'Gogte Circle', 'Rani Channamma Circle', 'Khasbag',
        'Sadashiv Nagar', 'Ashok Nagar', 'Basaveshwar Nagar', 'Shivaji Nagar'
    ],
    
    # Maharashtra
    'Mumbai': [
        'Andheri', 'Bandra', 'Powai', 'Juhu', 'Vile Parle', 'Goregaon',
        'Malad', 'Kandivali', 'Borivali', 'Dahisar', 'Mira Road', 'Bhayandar',
        'Chembur', 'Ghatkopar', 'Vikhroli', 'Bhandup', 'Mulund', 'Thane',
        'Navi Mumbai', 'Kharghar', 'Panvel', 'Nerul', 'Vashi', 'Airoli',
        'Kurla', 'Santacruz', 'Khar', 'Versova', 'Lokhandwala', 'Oshiwara',
        'Jogeshwari', 'Goregaon East', 'Goregaon West', 'Malad East', 'Malad West',
        'Kandivali East', 'Kandivali West', 'Borivali East', 'Borivali West',
        'Dahisar East', 'Dahisar West', 'Mira Road East', 'Mira Road West',
        'Bhayandar East', 'Bhayandar West', 'Chembur East', 'Chembur West',
        'Ghatkopar East', 'Ghatkopar West', 'Vikhroli East', 'Vikhroli West',
        'Bhandup East', 'Bhandup West', 'Mulund East', 'Mulund West',
        'Thane West', 'Thane East', 'Airoli', 'Koparkhairane', 'Sanpada',
        'Seawoods', 'Belapur', 'CBD Belapur', 'Kharghar Sector', 'Kamothe',
        'Ulwe', 'Dronagiri', 'Kalamboli', 'Taloja', 'Kharghar'
    ],
    'Pune': [
        'Hinjawadi', 'Wakad', 'Baner', 'Aundh', 'Kothrud', 'Karve Nagar',
        'Deccan', 'FC Road', 'JM Road', 'Koregaon Park', 'Viman Nagar',
        'Kalyani Nagar', 'Kharadi', 'Wagholi', 'Hadapsar', 'Magarpatta',
        'Amanora', 'Hadapsar', 'Kondhwa', 'Wanowrie', 'Mohammedwadi',
        'Katraj', 'Dhankawadi', 'Sinhagad Road', 'Bavdhan', 'Sus Road',
        'Pashan', 'Baner Road', 'Balewadi', 'Hinjewadi Phase 1', 'Hinjewadi Phase 2',
        'Hinjewadi Phase 3', 'Ravet', 'Tathawade', 'Chakan', 'Talegaon',
        'Kharadi', 'Viman Nagar', 'Kalyani Nagar', 'Koregaon Park', 'Deccan Gymkhana',
        'Shivajinagar', 'Camp', 'Sadashiv Peth', 'Shaniwar Peth', 'Kasba Peth',
        'Bibwewadi', 'Sahakar Nagar', 'Warje', 'NIBM', 'Undri', 'Pisoli'
    ],
    'Nagpur': [
        'Civil Lines', 'Dharampeth', 'Ramdaspeth', 'Shankar Nagar', 'Wardha Road',
        'Amravati Road', 'Kamptee Road', 'Katol Road', 'Hingna Road', 'Butibori',
        'Mihan', 'Khapri', 'Wardha Road', 'Amravati Road', 'Kamptee Road'
    ],
    'Nashik': [
        'Gangapur Road', 'College Road', 'Satpur', 'Ambad', 'CIDCO',
        'Nashik Road', 'Panchavati', 'Old Nashik', 'New Nashik', 'Trimbak Road'
    ],
    
    # Tamil Nadu
    'Chennai': [
        'T Nagar', 'Anna Nagar', 'Adyar', 'Besant Nagar', 'Velachery',
        'OMR', 'ECR', 'Porur', 'Poonamallee', 'Ambattur', 'Avadi',
        'Tambaram', 'Chrompet', 'Pallavaram', 'Guindy', 'Saidapet',
        'Mylapore', 'Nungambakkam', 'Kilpauk', 'Aminjikarai', 'Purasawalkam',
        'Perambur', 'Vyasarpadi', 'Washermanpet', 'Tondiarpet', 'Royapuram',
        'Egmore', 'Mount Road', 'Nandanam', 'Alwarpet', 'Boat Club',
        'RA Puram', 'Mylapore', 'Triplicane', 'Chepauk', 'Marina Beach',
        'Thiruvanmiyur', 'Kottivakkam', 'Palavakkam', 'Neelankarai', 'Sholinganallur',
        'Perungudi', 'Thoraipakkam', 'Pallikaranai', 'Medavakkam', 'Kovilambakkam',
        'Keelkattalai', 'Tambaram', 'Chrompet', 'Pallavaram', 'St. Thomas Mount',
        'Guindy', 'Saidapet', 'Koyambedu', 'Anna Nagar East', 'Anna Nagar West',
        'Anna Nagar', 'KK Nagar', 'Ashok Nagar', 'Vadapalani', 'Aminjikarai',
        'Kilpauk', 'Chetpet', 'Nungambakkam', 'T Nagar', 'Mylapore',
        'Alwarpet', 'Boat Club', 'RA Puram', 'Adyar', 'Besant Nagar'
    ],
    'Coimbatore': [
        'RS Puram', 'Saibaba Colony', 'Race Course', 'Gandhipuram', 'Peelamedu',
        'Saravanampatti', 'Sitra', 'Kovaipudur', 'Singanallur', 'Gandhipuram',
        'Town Hall', 'Ukkadam', 'Ramanathapuram', 'Sundarapuram', 'Sulur',
        'Karamadai', 'Mettupalayam', 'Pollachi', 'Udumalpet'
    ],
    'Madurai': [
        'Anna Nagar', 'KK Nagar', 'Villapuram', 'Tallakulam', 'Goripalayam',
        'Simmakkal', 'Periyar', 'Teppakulam', 'Thirumangalam', 'Koodal Nagar'
    ],
    
    # Telangana
    'Hyderabad': [
        'Gachibowli', 'Hitech City', 'Madhapur', 'Kondapur', 'Jubilee Hills',
        'Banjara Hills', 'Himayatnagar', 'Abids', 'Secunderabad', 'Begumpet',
        'Ameerpet', 'Kukatpally', 'Miyapur', 'Alwal', 'Bachupally',
        'Nizampet', 'Qutubullapur', 'Bachupally', 'Kompally', 'Suchitra',
        'Boduppal', 'Uppal', 'Nagole', 'LB Nagar', 'Dilsukhnagar',
        'Malakpet', 'Charminar', 'Old City', 'Mehdipatnam', 'Tolichowki',
        'Rajendra Nagar', 'Attapur', 'Narsingi', 'Manikonda', 'Nanakramguda',
        'Financial District', 'Nanakramguda', 'Kokapet', 'Tellapur', 'Narsingi',
        'Manikonda', 'Gachibowli', 'Hitech City', 'Madhapur', 'Kondapur',
        'Jubilee Hills', 'Banjara Hills', 'Himayatnagar', 'Abids', 'Secunderabad',
        'Begumpet', 'Ameerpet', 'Kukatpally', 'Miyapur', 'Alwal'
    ],
    'Warangal': [
        'Hanamkonda', 'Kazipet', 'Subedari', 'Enumamula', 'Narsampet'
    ],
    
    # Delhi NCR
    'New Delhi': [
        'Connaught Place', 'Karol Bagh', 'Rajendra Place', 'Punjabi Bagh',
        'Paschim Vihar', 'Janakpuri', 'Dwarka', 'Rohini', 'Pitampura',
        'Model Town', 'GTB Nagar', 'Kamla Nagar', 'Hudson Lane', 'Kingsway Camp',
        'Civil Lines', 'Kashmere Gate', 'Old Delhi', 'Chandni Chowk', 'Daryaganj',
        'ITO', 'Mandir Marg', 'Patel Nagar', 'Rajouri Garden', 'Vikaspuri',
        'Uttam Nagar', 'Nangloi', 'Najafgarh', 'Dwarka Sector', 'Rohini Sector',
        'Pitampura', 'Model Town', 'GTB Nagar', 'Kamla Nagar', 'Hudson Lane'
    ],
    'Delhi': [
        'Connaught Place', 'Karol Bagh', 'Rajendra Place', 'Punjabi Bagh',
        'Paschim Vihar', 'Janakpuri', 'Dwarka', 'Rohini', 'Pitampura',
        'Model Town', 'GTB Nagar', 'Kamla Nagar', 'Hudson Lane', 'Kingsway Camp',
        'Civil Lines', 'Kashmere Gate', 'Old Delhi', 'Chandni Chowk', 'Daryaganj',
        'ITO', 'Mandir Marg', 'Patel Nagar', 'Rajouri Garden', 'Vikaspuri',
        'Uttam Nagar', 'Nangloi', 'Najafgarh', 'Dwarka Sector', 'Rohini Sector'
    ],
    'Gurgaon': [
        'DLF Phase 1', 'DLF Phase 2', 'DLF Phase 3', 'DLF Phase 4', 'DLF Phase 5',
        'Sector 14', 'Sector 15', 'Sector 17', 'Sector 18', 'Sector 22',
        'Sector 23', 'Sector 29', 'Sector 31', 'Sector 43', 'Sector 44',
        'Sector 45', 'Sector 46', 'Sector 47', 'Sector 48', 'Sector 49',
        'Sector 50', 'Sector 51', 'Sector 52', 'Sector 53', 'Sector 54',
        'Sector 55', 'Sector 56', 'Sector 57', 'Sector 58', 'Sector 59',
        'Sector 60', 'Sector 61', 'Sector 62', 'Sector 63', 'Sector 64',
        'Sector 65', 'Sector 66', 'Sector 67', 'Sector 68', 'Sector 69',
        'Sector 70', 'Sector 71', 'Sector 72', 'Sector 73', 'Sector 74',
        'Sector 75', 'Sector 76', 'Sector 77', 'Sector 78', 'Sector 79',
        'Sector 80', 'Sector 81', 'Sector 82', 'Sector 83', 'Sector 84',
        'Sector 85', 'Sector 86', 'Sector 87', 'Sector 88', 'Sector 89',
        'Sector 90', 'Sector 91', 'Sector 92', 'Sector 93', 'Sector 94',
        'Sector 95', 'Sector 96', 'Sector 97', 'Sector 98', 'Sector 99',
        'Sector 100', 'Sector 101', 'Sector 102', 'Sector 103', 'Sector 104',
        'Sector 105', 'Sector 106', 'Sector 107', 'Sector 108', 'Sector 109',
        'Sector 110', 'Sector 111', 'Sector 112', 'Sector 113', 'Sector 114',
        'Sector 115', 'MG Road', 'Old Gurgaon', 'New Gurgaon', 'Gurgaon City',
        'Palam Vihar', 'Sushant Lok', 'DLF City', 'Sohna Road', 'Golf Course Road',
        'Golf Course Extension Road', 'Southern Peripheral Road', 'Northern Peripheral Road',
        'Dwarka Expressway', 'NH-8', 'Sohna', 'Faridabad Road', 'Pataudi Road'
    ],
    'Gurugram': [
        'DLF Phase 1', 'DLF Phase 2', 'DLF Phase 3', 'DLF Phase 4', 'DLF Phase 5',
        'Sector 14', 'Sector 15', 'Sector 17', 'Sector 18', 'Sector 22',
        'Sector 23', 'Sector 29', 'Sector 31', 'Sector 43', 'Sector 44',
        'Sector 45', 'Sector 46', 'Sector 47', 'Sector 48', 'Sector 49',
        'Sector 50', 'Sector 51', 'Sector 52', 'Sector 53', 'Sector 54',
        'Sector 55', 'Sector 56', 'Sector 57', 'Sector 58', 'Sector 59',
        'Sector 60', 'Sector 61', 'Sector 62', 'Sector 63', 'Sector 64',
        'Sector 65', 'Sector 66', 'Sector 67', 'Sector 68', 'Sector 69',
        'Sector 70', 'Sector 71', 'Sector 72', 'Sector 73', 'Sector 74',
        'Sector 75', 'Sector 76', 'Sector 77', 'Sector 78', 'Sector 79',
        'Sector 80', 'Sector 81', 'Sector 82', 'Sector 83', 'Sector 84',
        'Sector 85', 'Sector 86', 'Sector 87', 'Sector 88', 'Sector 89',
        'Sector 90', 'Sector 91', 'Sector 92', 'Sector 93', 'Sector 94',
        'Sector 95', 'Sector 96', 'Sector 97', 'Sector 98', 'Sector 99',
        'Sector 100', 'Sector 101', 'Sector 102', 'Sector 103', 'Sector 104',
        'Sector 105', 'Sector 106', 'Sector 107', 'Sector 108', 'Sector 109',
        'Sector 110', 'Sector 111', 'Sector 112', 'Sector 113', 'Sector 114',
        'Sector 115', 'MG Road', 'Old Gurgaon', 'New Gurgaon', 'Gurgaon City',
        'Palam Vihar', 'Sushant Lok', 'DLF City', 'Sohna Road', 'Golf Course Road',
        'Golf Course Extension Road', 'Southern Peripheral Road', 'Northern Peripheral Road',
        'Dwarka Expressway', 'NH-8', 'Sohna', 'Faridabad Road', 'Pataudi Road'
    ],
    'Noida': [
        'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5',
        'Sector 6', 'Sector 7', 'Sector 8', 'Sector 9', 'Sector 10',
        'Sector 11', 'Sector 12', 'Sector 13', 'Sector 14', 'Sector 15',
        'Sector 16', 'Sector 17', 'Sector 18', 'Sector 19', 'Sector 20',
        'Sector 21', 'Sector 22', 'Sector 23', 'Sector 24', 'Sector 25',
        'Sector 26', 'Sector 27', 'Sector 28', 'Sector 29', 'Sector 30',
        'Sector 31', 'Sector 32', 'Sector 33', 'Sector 34', 'Sector 35',
        'Sector 36', 'Sector 37', 'Sector 38', 'Sector 39', 'Sector 40',
        'Sector 41', 'Sector 42', 'Sector 43', 'Sector 44', 'Sector 45',
        'Sector 46', 'Sector 47', 'Sector 48', 'Sector 49', 'Sector 50',
        'Sector 51', 'Sector 52', 'Sector 53', 'Sector 54', 'Sector 55',
        'Sector 56', 'Sector 57', 'Sector 58', 'Sector 59', 'Sector 60',
        'Sector 61', 'Sector 62', 'Sector 63', 'Sector 64', 'Sector 65',
        'Sector 66', 'Sector 67', 'Sector 68', 'Sector 69', 'Sector 70',
        'Sector 71', 'Sector 72', 'Sector 73', 'Sector 74', 'Sector 75',
        'Sector 76', 'Sector 77', 'Sector 78', 'Sector 79', 'Sector 80',
        'Sector 81', 'Sector 82', 'Sector 83', 'Sector 84', 'Sector 85',
        'Sector 86', 'Sector 87', 'Sector 88', 'Sector 89', 'Sector 90',
        'Sector 91', 'Sector 92', 'Sector 93', 'Sector 94', 'Sector 95',
        'Sector 96', 'Sector 97', 'Sector 98', 'Sector 99', 'Sector 100',
        'Sector 101', 'Sector 102', 'Sector 103', 'Sector 104', 'Sector 105',
        'Sector 106', 'Sector 107', 'Sector 108', 'Sector 109', 'Sector 110',
        'Sector 111', 'Sector 112', 'Sector 113', 'Sector 114', 'Sector 115',
        'Sector 116', 'Sector 117', 'Sector 118', 'Sector 119', 'Sector 120',
        'Sector 121', 'Sector 122', 'Sector 123', 'Sector 124', 'Sector 125',
        'Sector 126', 'Sector 127', 'Sector 128', 'Sector 129', 'Sector 130',
        'Sector 131', 'Sector 132', 'Sector 133', 'Sector 134', 'Sector 135',
        'Sector 136', 'Sector 137', 'Sector 138', 'Sector 139', 'Sector 140',
        'Sector 141', 'Sector 142', 'Sector 143', 'Sector 144', 'Sector 145',
        'Sector 146', 'Sector 147', 'Sector 148', 'Sector 149', 'Sector 150',
        'Sector 151', 'Sector 152', 'Sector 153', 'Sector 154', 'Sector 155',
        'Sector 156', 'Sector 157', 'Sector 158', 'Sector 159', 'Sector 160',
        'Sector 161', 'Sector 162', 'Sector 163', 'Sector 164', 'Sector 165',
        'Sector 166', 'Sector 167', 'Sector 168', 'Sector 169', 'Sector 170',
        'Sector 171', 'Sector 172', 'Sector 173', 'Sector 174', 'Sector 175',
        'Greater Noida', 'Noida Extension', 'Noida City Centre', 'Noida Sector 18',
        'Noida Sector 62', 'Noida Sector 137', 'Noida Sector 143', 'Noida Sector 150',
        'Noida Sector 168', 'Noida Sector 76', 'Noida Sector 77', 'Noida Sector 78'
    ],
    
    # Gujarat
    'Ahmedabad': [
        'Satellite', 'Bopal', 'Bodakdev', 'Prahlad Nagar', 'Vastrapur',
        'Gurukul', 'Memnagar', 'Navrangpura', 'CG Road', 'SG Highway',
        'Science City', 'Thaltej', 'Shilaj', 'Bavla', 'Sanand',
        'Gandhinagar', 'Sarkhej', 'Jodhpur', 'Vejalpur', 'Ghatlodia',
        'Naranpura', 'Nava Vadaj', 'Sola', 'Sarkhej', 'Bopal',
        'Bodakdev', 'Prahlad Nagar', 'Vastrapur', 'Gurukul', 'Memnagar'
    ],
    'Surat': [
        'Adajan', 'Athwa', 'Piplod', 'Vesu', 'Pal',
        'Varachha', 'Katargam', 'Udhna', 'Sachin', 'Dumas',
        'Magob', 'Hazira', 'Bamroli', 'Palanpur', 'Bardoli'
    ],
    'Vadodara': [
        'Alkapuri', 'Fatehgunj', 'Sayajigunj', 'Akota', 'Makarpura',
        'Gotri', 'Waghodia', 'Harni', 'Karelibaug', 'Tandalja'
    ],
    
    # West Bengal
    'Kolkata': [
        'Salt Lake', 'New Town', 'Rajarhat', 'Howrah', 'Dum Dum',
        'Barasat', 'Kalyani', 'Bidhannagar', 'Behala', 'Alipore',
        'Park Street', 'Esplanade', 'BBD Bagh', 'Dalhousie', 'Chowringhee',
        'Tollygunge', 'Garia', 'Jadavpur', 'Santoshpur', 'Bansdroni',
        'Narendrapur', 'Sonarpur', 'Baruipur', 'Diamond Harbour', 'Kakdwip'
    ],
    
    # Rajasthan
    'Jaipur': [
        'Malviya Nagar', 'C Scheme', 'Bani Park', 'Vaishali Nagar', 'Mansarovar',
        'Vidhyadhar Nagar', 'Sitapura', 'Mahapura', 'Ajmer Road', 'Tonk Road',
        'Sanganer', 'Amer', 'Jhotwara', 'Raja Park', 'Pink City',
        'Walled City', 'MI Road', 'Ajmeri Gate', 'Chandpole', 'Hawa Mahal'
    ],
    'Jodhpur': [
        'Basni', 'Ratanada', 'Shastri Nagar', 'Shastri Circle', 'Umaid Bhawan',
        'Pal Road', 'Mandore', 'Bilara', 'Phalodi', 'Osian'
    ],
    
    # Andhra Pradesh
    'Visakhapatnam': [
        'Dwaraka Nagar', 'MVP Colony', 'Seethammadhara', 'Madhurawada', 'Gajuwaka',
        'Maddilapalem', 'Akkayyapalem', 'Lawson Bay Colony', 'Beach Road', 'Rushikonda'
    ],
    'Vijayawada': [
        'Benz Circle', 'MG Road', 'Eluru Road', 'Gunadala', 'Patamata',
        'Nidamanuru', 'Poranki', 'Kanuru', 'Bhavanipuram', 'Auto Nagar'
    ],
    
    # Kerala
    'Kochi': [
        'Marine Drive', 'Fort Kochi', 'Mattancherry', 'Ernakulam', 'Edapally',
        'Kakkanad', 'Infopark', 'Smart City', 'Vyttila', 'Palarivattom',
        'Kaloor', 'MG Road', 'Banerji Road', 'Chittoor Road', 'Panampilly Nagar'
    ],
    
    # Add more cities as needed
}

def get_localities_for_city(city_name):
    """
    Get localities for a given city name.
    Returns a list of localities or empty list if city not found.
    
    Args:
        city_name (str): Name of the city (case-insensitive)
    
    Returns:
        list: List of locality names for the city
    """
    if not city_name:
        return []
    
    # Normalize city name (trim whitespace)
    city_normalized = city_name.strip()
    
    # Debug: Print available city keys for troubleshooting
    available_cities = list(CITY_LOCALITIES.keys())
    
    # Try exact match first (case-sensitive)
    if city_normalized in CITY_LOCALITIES:
        print(f"[City Mapping] Exact match found for '{city_normalized}'")
        return CITY_LOCALITIES[city_normalized].copy()
    
    # Try case-insensitive exact match
    for city_key, localities in CITY_LOCALITIES.items():
        if city_key.lower() == city_normalized.lower():
            print(f"[City Mapping] Case-insensitive match found: '{city_key}' for '{city_normalized}'")
            return localities.copy()
    
    # Try partial match (in case city name has variations like "Bengaluru" vs "Bangalore")
    city_lower = city_normalized.lower()
    for city_key, localities in CITY_LOCALITIES.items():
        city_key_lower = city_key.lower()
        # Check if one contains the other (for variations)
        if city_lower in city_key_lower or city_key_lower in city_lower:
            # Make sure it's a meaningful match (not just a single character)
            if len(city_lower) > 3 and len(city_key_lower) > 3:
                print(f"[City Mapping] Partial match found: '{city_key}' for '{city_normalized}'")
                return localities.copy()
    
    # No match found - log for debugging
    print(f"[City Mapping] No match found for '{city_normalized}'. Available cities: {available_cities[:10]}...")
    return []

def get_all_cities():
    """
    Get all cities that have localities defined.
    
    Returns:
        list: List of city names
    """
    return list(CITY_LOCALITIES.keys())
