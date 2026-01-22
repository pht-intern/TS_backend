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
    'Gulbarga': [
        'Gulbarga City', 'Shahabad', 'Aland', 'Sedam', 'Chittapur',
        'Jevargi', 'Shorapur', 'Yadgir', 'Shahpur', 'Aland Road',
        'Station Road', 'Super Market', 'Gandhi Chowk', 'Mahatma Gandhi Road',
        'Basavakalyan Road', 'Ring Road', 'Airport Road', 'Medical College Road'
    ],
    'Kalaburagi': [
        'Gulbarga City', 'Shahabad', 'Aland', 'Sedam', 'Chittapur',
        'Jevargi', 'Shorapur', 'Yadgir', 'Shahpur', 'Aland Road',
        'Station Road', 'Super Market', 'Gandhi Chowk', 'Mahatma Gandhi Road',
        'Basavakalyan Road', 'Ring Road', 'Airport Road', 'Medical College Road'
    ],
    'Davangere': [
        'Davangere City', 'Chitradurga Road', 'Bhadravathi Road', 'Harihar',
        'Honnali', 'Jagalur', 'Harapanahalli', 'Mayakonda', 'Nyamathi',
        'Station Road', 'MG Road', 'Bapuji Nagar', 'Shivaji Nagar',
        'Gandhi Nagar', 'Ashok Nagar', 'Vidyanagar', 'Kuvempu Nagar',
        'BTM Layout', 'Kuvempu Extension', 'Ring Road'
    ],
    'Shimoga': [
        'Shimoga City', 'Bhadravathi', 'Sagar', 'Tirthahalli', 'Hosanagara',
        'Shikaripura', 'Sorab', 'Hosanagara', 'Thirthahalli', 'Sagara',
        'MG Road', 'Station Road', 'Gandhi Bazaar', 'Kuvempu Road',
        'Sagar Road', 'Bhadravathi Road', 'Tirthahalli Road', 'Ring Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Shivamogga': [
        'Shimoga City', 'Bhadravathi', 'Sagar', 'Tirthahalli', 'Hosanagara',
        'Shikaripura', 'Sorab', 'Hosanagara', 'Thirthahalli', 'Sagara',
        'MG Road', 'Station Road', 'Gandhi Bazaar', 'Kuvempu Road',
        'Sagar Road', 'Bhadravathi Road', 'Tirthahalli Road', 'Ring Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Tumkur': [
        'Tumkur City', 'Kunigal', 'Gubbi', 'Sira', 'Pavagada',
        'Madhugiri', 'Koratagere', 'Tiptur', 'Turuvekere', 'Chiknayakanhalli',
        'MG Road', 'Station Road', 'B H Road', 'Banglore Road',
        'Mysore Road', 'Ring Road', 'Vidyanagar', 'Ashok Nagar',
        'Shivaji Nagar', 'Gandhi Nagar', 'Kuvempu Nagar'
    ],
    'Tumakuru': [
        'Tumkur City', 'Kunigal', 'Gubbi', 'Sira', 'Pavagada',
        'Madhugiri', 'Koratagere', 'Tiptur', 'Turuvekere', 'Chiknayakanhalli',
        'MG Road', 'Station Road', 'B H Road', 'Banglore Road',
        'Mysore Road', 'Ring Road', 'Vidyanagar', 'Ashok Nagar',
        'Shivaji Nagar', 'Gandhi Nagar', 'Kuvempu Nagar'
    ],
    'Udupi': [
        'Udupi City', 'Manipal', 'Kaup', 'Karkala', 'Kundapura',
        'Baindoor', 'Hebri', 'Brahmavar', 'Byndoor', 'Gangolli',
        'MG Road', 'Car Street', 'Malpe', 'Kapu', 'Padubidri',
        'Kota', 'Shirva', 'Parkala', 'Yenepoya', 'Manipal University Area'
    ],
    'Raichur': [
        'Raichur City', 'Lingsugur', 'Sindhnur', 'Manvi', 'Devadurga',
        'Mudgal', 'Kushtagi', 'Gangavathi', 'Yelburga', 'Koppal',
        'Station Road', 'MG Road', 'Ring Road', 'Airport Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bidar': [
        'Bidar City', 'Basavakalyan', 'Bhalki', 'Humnabad', 'Aurad',
        'Kamalnagar', 'Chitgoppa', 'Bidar Fort', 'Gurudwara Road',
        'Station Road', 'MG Road', 'Ring Road', 'Airport Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bijapur': [
        'Bijapur City', 'Basavana Bagevadi', 'Muddebihal', 'Sindgi',
        'Indi', 'Tikota', 'Talikoti', 'Devar Hippargi', 'Babaleshwar',
        'Station Road', 'MG Road', 'Gol Gumbaz Road', 'Ring Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Vijayapura': [
        'Bijapur City', 'Basavana Bagevadi', 'Muddebihal', 'Sindgi',
        'Indi', 'Tikota', 'Talikoti', 'Devar Hippargi', 'Babaleshwar',
        'Station Road', 'MG Road', 'Gol Gumbaz Road', 'Ring Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chitradurga': [
        'Chitradurga City', 'Hiriyur', 'Holalkere', 'Hosadurga', 'Molakalmuru',
        'Challakere', 'Hiriyur', 'Holalkere', 'Hosadurga', 'Molakalmuru',
        'Station Road', 'MG Road', 'Ring Road', 'Fort Area',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Hassan': [
        'Hassan City', 'Arsikere', 'Belur', 'Channarayapatna', 'Holenarasipura',
        'Sakleshpur', 'Alur', 'Arkalgud', 'Arakere', 'Bettadahalli',
        'Station Road', 'MG Road', 'Ring Road', 'Belur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mandya': [
        'Mandya City', 'Maddur', 'Malavalli', 'Pandavapura', 'Srirangapatna',
        'Krishnarajpet', 'Nagamangala', 'Bellur', 'Melukote', 'Kokkare Bellur',
        'Station Road', 'MG Road', 'Ring Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chikkamagaluru': [
        'Chikkamagaluru City', 'Kadur', 'Mudigere', 'Narasimharajapura', 'Sringeri',
        'Tarikere', 'Koppa', 'Balehonnur', 'Ajampura', 'Aldur',
        'Station Road', 'MG Road', 'Ring Road', 'Coffee Board Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kolar': [
        'Kolar City', 'Bangarapet', 'Malur', 'Mulbagal', 'Srinivaspur',
        'Chintamani', 'Gudibanda', 'Bagepalli', 'Kolar Gold Fields', 'Robertsonpet',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ballari': [
        'Ballari City', 'Hospet', 'Sandur', 'Kudligi', 'Hagaribommanahalli',
        'Hosapete', 'Toranagallu', 'Bellary Fort', 'Cantonment Area',
        'Station Road', 'MG Road', 'Ring Road', 'Hospet Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bellary': [
        'Ballari City', 'Hospet', 'Sandur', 'Kudligi', 'Hagaribommanahalli',
        'Hosapete', 'Toranagallu', 'Bellary Fort', 'Cantonment Area',
        'Station Road', 'MG Road', 'Ring Road', 'Hospet Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bagalkot': [
        'Bagalkot City', 'Badami', 'Hungund', 'Jamkhandi', 'Mudhol',
        'Bilgi', 'Guledgudda', 'Ilkal', 'Kerur', 'Mahalingpur',
        'Station Road', 'MG Road', 'Ring Road', 'Badami Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Gadag': [
        'Gadag City', 'Betageri', 'Mundargi', 'Nargund', 'Ron',
        'Shirahatti', 'Lakshmeshwar', 'Gajendragad', 'Hirekerur', 'Hulsoor',
        'Station Road', 'MG Road', 'Ring Road', 'Hubli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Haveri': [
        'Haveri City', 'Byadgi', 'Hangal', 'Hirekerur', 'Ranebennur',
        'Savanur', 'Shiggaon', 'Bankapura', 'Hirekerur', 'Rattihalli',
        'Station Road', 'MG Road', 'Ring Road', 'Hubli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Koppal': [
        'Koppal City', 'Gangavathi', 'Yelburga', 'Kushtagi', 'Kanakagiri',
        'Kuknur', 'Karatagi', 'Gangavathi', 'Yelburga', 'Kushtagi',
        'Station Road', 'MG Road', 'Ring Road', 'Raichur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Yadgir': [
        'Yadgir City', 'Shahpur', 'Shorapur', 'Gurmitkal', 'Hunsagi',
        'Wadi', 'Chincholi', 'Sedam', 'Jevargi', 'Shahpur',
        'Station Road', 'MG Road', 'Ring Road', 'Gulbarga Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chamarajanagar': [
        'Chamarajanagar City', 'Gundlupet', 'Kollegal', 'Yelandur', 'Hanur',
        'Biligirirangana Betta', 'BR Hills', 'Gundlupet', 'Kollegal', 'Yelandur',
        'Station Road', 'MG Road', 'Ring Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kodagu': [
        'Madikeri', 'Virajpet', 'Somwarpet', 'Kushalnagar', 'Gonikoppal',
        'Ponnampet', 'Bhagamandala', 'Talacauvery', 'Abbey Falls', 'Raja Seat',
        'MG Road', 'Station Road', 'Ring Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Coorg': [
        'Madikeri', 'Virajpet', 'Somwarpet', 'Kushalnagar', 'Gonikoppal',
        'Ponnampet', 'Bhagamandala', 'Talacauvery', 'Abbey Falls', 'Raja Seat',
        'MG Road', 'Station Road', 'Ring Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Madikeri': [
        'Madikeri City', 'Virajpet', 'Somwarpet', 'Kushalnagar', 'Gonikoppal',
        'Ponnampet', 'Bhagamandala', 'Talacauvery', 'Abbey Falls', 'Raja Seat',
        'MG Road', 'Station Road', 'Ring Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ramanagara': [
        'Ramanagara City', 'Channapatna', 'Kanakapura', 'Magadi', 'Bidadi',
        'Harohalli', 'Doddaballapur', 'Nelamangala', 'Kanakapura', 'Magadi',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chikkaballapur': [
        'Chikkaballapur City', 'Bagepalli', 'Gauribidanur', 'Gudibanda', 'Sidlaghatta',
        'Chintamani', 'Shidlaghatta', 'Bagepalli', 'Gauribidanur', 'Gudibanda',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Vijayanagara': [
        'Hosapete', 'Hospet', 'Kamalapura', 'Anegundi', 'Hampi',
        'Toranagallu', 'Sandur', 'Kudligi', 'Hagaribommanahalli', 'Bellary',
        'Station Road', 'MG Road', 'Ring Road', 'Hampi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Hosapete': [
        'Hosapete City', 'Hospet', 'Kamalapura', 'Anegundi', 'Hampi',
        'Toranagallu', 'Sandur', 'Kudligi', 'Hagaribommanahalli', 'Bellary',
        'Station Road', 'MG Road', 'Ring Road', 'Hampi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Hospet': [
        'Hosapete City', 'Hospet', 'Kamalapura', 'Anegundi', 'Hampi',
        'Toranagallu', 'Sandur', 'Kudligi', 'Hagaribommanahalli', 'Bellary',
        'Station Road', 'MG Road', 'Ring Road', 'Hampi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Dharwad': [
        'Dharwad City', 'Hubballi', 'Navalgund', 'Kundgol', 'Kalghatgi',
        'Alnavar', 'Annigeri', 'Hubballi', 'Navalgund', 'Kundgol',
        'Station Road', 'MG Road', 'Ring Road', 'Hubli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bangalore': [
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
    'Mysore': [
        'Vijayanagar', 'Kuvempunagar', 'Gokulam', 'Nazarbad', 'Saraswathipuram',
        'Vishweshwarapuram', 'Yadavagiri', 'T K Layout', 'Bannimantap', 'Hunsur Road',
        'Bogadi', 'Hinkal', 'Kuvempunagar Extension', 'JP Nagar', 'Vontikoppal',
        'Lakshmipuram', 'Krishnamurthypuram', 'Mandi Mohalla', 'Devaraja Market',
        'Chamarajapuram', 'Ashokapuram', 'Siddharthanagar', 'Vijayanagar 1st Stage',
        'Vijayanagar 2nd Stage', 'Vijayanagar 3rd Stage', 'Vijayanagar 4th Stage'
    ],
    'Mangalore': [
        'Kadri', 'Bejai', 'Pandeshwar', 'Hampankatta', 'Kankanady',
        'Bendoor', 'Falnir', 'Kodialbail', 'Bolar', 'Urwa',
        'Kulur', 'Padil', 'Bondel', 'Kottara', 'Jeppu',
        'Kadri Park', 'Light House Hill', 'Pumpwell', 'Kankanady', 'Attavar'
    ],
    'Hubli': [
        'Vidyanagar', 'Gokul Road', 'Deshpande Nagar', 'Keshwapur', 'Hubballi City',
        'Old Hubballi', 'New Hubballi', 'Unkal', 'Bengeri', 'Dharwad Road',
        'Airport Road', 'Gandhi Nagar', 'Keshwapur Extension', 'Keshwapur Main',
        'Vidyanagar Extension', 'Gokul Road Extension'
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
        'Nashik Road', 'Panchavati', 'Old Nashik', 'New Nashik', 'Trimbak Road',
        'Dwarka', 'Gangapur', 'Nashik City', 'Upnagar', 'Indira Nagar',
        'Sharanpur', 'Canada Corner', 'Ashok Stambh', 'Mahatma Nagar', 'Pathardi Phata'
    ],
    'Aurangabad': [
        'Aurangabad City', 'Cidco', 'Jalna Road', 'Beed Bypass', 'Paithan Road',
        'Station Road', 'MG Road', 'Kranti Chowk', 'Gulmandi', 'N-2 Cidco',
        'N-4 Cidco', 'N-5 Cidco', 'N-6 Cidco', 'N-9 Cidco', 'N-12 Cidco',
        'Samarth Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Ashok Nagar', 'Vidyanagar',
        'Bibika Maqbara', 'Daulatabad', 'Ellora', 'Ajanta', 'Aurangabad Cantonment'
    ],
    'Solapur': [
        'Solapur City', 'Station Road', 'MG Road', 'Pandharpur Road', 'Bijapur Road',
        'Akkalkot Road', 'Barshi Road', 'Sangola Road', 'Mangalwedha Road', 'Madha Road',
        'Shivaji Nagar', 'Gandhi Nagar', 'Ashok Nagar', 'Vidyanagar', 'Kuvempu Nagar',
        'Ring Road', 'Airport Road', 'Industrial Area', 'MIDC', 'Solapur Cantonment'
    ],
    'Thane': [
        'Thane West', 'Thane East', 'Kopri', 'Naupada', 'Wagle Estate',
        'Majiwada', 'Kolshet', 'Balkum', 'Kasarvadavali', 'Ghodbunder Road',
        'Pokhran Road', 'Ghodbunder', 'Manpada', 'Hiranandani Estate', 'Vasant Vihar',
        'Brahmand', 'Hiranandani Meadows', 'Hiranandani Gardens', 'Lokmanya Nagar', 'Kopri'
    ],
    'Pimpri-Chinchwad': [
        'Pimpri', 'Chinchwad', 'Nigdi', 'Akurdi', 'Ravet',
        'Tathawade', 'Wakad', 'Hinjawadi', 'Bhosari', 'Chikhali',
        'Sangvi', 'Rahatani', 'Pimple Saudagar', 'Pimple Gurav', 'Pimple Nilakh',
        'Rahatani', 'Kalewadi', 'Thergaon', 'Dange Chowk', 'MIDC'
    ],
    'Kalyan': [
        'Kalyan West', 'Kalyan East', 'Kalyan Station', 'Dombivli', 'Ulhasnagar',
        'Ambernath', 'Badlapur', 'Titwala', 'Shahad', 'Vithalwadi',
        'Kopar', 'Khadakpada', 'Mahatma Phule Chowk', 'Shivaji Chowk', 'Gandhi Chowk',
        'Station Road', 'MG Road', 'Ring Road', 'Agasan', 'Kalyan Shilphata'
    ],
    'Vasai-Virar': [
        'Vasai', 'Virar', 'Nalasopara', 'Naigaon', 'Bhayandar',
        'Mira Road', 'Boisar', 'Palghar', 'Bassein', 'Manickpur',
        'Virar East', 'Virar West', 'Vasai Road', 'Nalasopara East', 'Nalasopara West',
        'Naigaon East', 'Naigaon West', 'Bhayandar East', 'Bhayandar West'
    ],
    'Navi Mumbai': [
        'Vashi', 'Nerul', 'Kharghar', 'Belapur', 'Panvel',
        'Airoli', 'Koparkhairane', 'Sanpada', 'Seawoods', 'Juinagar',
        'CBD Belapur', 'Kharghar Sector', 'Kamothe', 'Ulwe', 'Dronagiri',
        'Kalamboli', 'Taloja', 'Kharghar', 'Nerul East', 'Nerul West',
        'Vashi Sector', 'Belapur CBD', 'Seawoods Darave', 'Kharghar Hills'
    ],
    'Amravati': [
        'Amravati City', 'Badnera', 'Chandur Bazar', 'Daryapur', 'Anjangaon',
        'Achalpur', 'Warud', 'Morshi', 'Chandur Railway', 'Nandgaon Khandeshwar',
        'Station Road', 'MG Road', 'Ring Road', 'Airport Road', 'Nagpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Kuvempu Nagar'
    ],
    'Kolhapur': [
        'Kolhapur City', 'Shiroli', 'Kagal', 'Ichalkaranji', 'Gadhinglaj',
        'Ajra', 'Radhanagari', 'Chandgad', 'Gaganbawda', 'Shahuwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Pune Road', 'Mumbai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Rajaram Nagar'
    ],
    'Sangli': [
        'Sangli City', 'Miraj', 'Tasgaon', 'Jath', 'Kavathe Mahankal',
        'Kadegaon', 'Khanapur', 'Atpadi', 'Walwa', 'Palus',
        'Station Road', 'MG Road', 'Ring Road', 'Pune Road', 'Kolhapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Miraj Station'
    ],
    'Jalgaon': [
        'Jalgaon City', 'Bhusawal', 'Erandol', 'Pachora', 'Chalisgaon',
        'Jamner', 'Amalner', 'Parola', 'Yawal', 'Raver',
        'Station Road', 'MG Road', 'Ring Road', 'Nashik Road', 'Dhule Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'MIDC'
    ],
    'Dhule': [
        'Dhule City', 'Nandurbar', 'Shirpur', 'Sakri', 'Shindkheda',
        'Sindkheda', 'Dondaicha', 'Shahada', 'Taloda', 'Navapur',
        'Station Road', 'MG Road', 'Ring Road', 'Nashik Road', 'Jalgaon Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nanded': [
        'Nanded City', 'Deglur', 'Mukhed', 'Kandhar', 'Loha',
        'Bhokar', 'Himayatnagar', 'Kinwat', 'Hadgaon', 'Mudkhed',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Aurangabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Gurudwara Area'
    ],
    'Latur': [
        'Latur City', 'Ahmadpur', 'Udgir', 'Nilanga', 'Ausa',
        'Chakur', 'Renapur', 'Jalkot', 'Shirur Anantpal', 'Deoni',
        'Station Road', 'MG Road', 'Ring Road', 'Aurangabad Road', 'Nanded Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Osmanabad': [
        'Osmanabad City', 'Tuljapur', 'Paranda', 'Bhum', 'Kalamb',
        'Washi', 'Lohara', 'Omerga', 'Tuljapur', 'Paranda',
        'Station Road', 'MG Road', 'Ring Road', 'Solapur Road', 'Aurangabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Beed': [
        'Beed City', 'Georai', 'Majalgaon', 'Parli', 'Ashti',
        'Patoda', 'Shirur Kasar', 'Wadwani', 'Dharur', 'Kaij',
        'Station Road', 'MG Road', 'Ring Road', 'Aurangabad Road', 'Latur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Jalna': [
        'Jalna City', 'Badnapur', 'Bhokardan', 'Partur', 'Ambad',
        'Ghansawangi', 'Jafferabad', 'Mantha', 'Badnapur', 'Bhokardan',
        'Station Road', 'MG Road', 'Ring Road', 'Aurangabad Road', 'Parbhani Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Parbhani': [
        'Parbhani City', 'Gangakhed', 'Palam', 'Pathri', 'Jintur',
        'Sonpeth', 'Purna', 'Sailu', 'Manwath', 'Parbhani',
        'Station Road', 'MG Road', 'Ring Road', 'Aurangabad Road', 'Nanded Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Hingoli': [
        'Hingoli City', 'Kalamnuri', 'Basmath', 'Sengaon', 'Aundha Nagnath',
        'Hingoli', 'Kalamnuri', 'Basmath', 'Sengaon', 'Aundha Nagnath',
        'Station Road', 'MG Road', 'Ring Road', 'Nanded Road', 'Parbhani Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ratnagiri': [
        'Ratnagiri City', 'Chiplun', 'Khed', 'Dapoli', 'Guhagar',
        'Rajapur', 'Sangameshwar', 'Lanja', 'Mandangad', 'Tala',
        'Station Road', 'MG Road', 'Ring Road', 'Mumbai Road', 'Goa Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Beach Area'
    ],
    'Sindhudurg': [
        'Malvan', 'Kankavli', 'Kudal', 'Vengurla', 'Devgad',
        'Sawantwadi', 'Dodamarg', 'Vaibhavwadi', 'Kankavli', 'Kudal',
        'Station Road', 'MG Road', 'Ring Road', 'Goa Road', 'Ratnagiri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Beach Area'
    ],
    'Satara': [
        'Satara City', 'Karad', 'Wai', 'Patan', 'Phaltan',
        'Koregaon', 'Mahabaleshwar', 'Pachgani', 'Rahimatpur', 'Khatav',
        'Station Road', 'MG Road', 'Ring Road', 'Pune Road', 'Kolhapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Sangamner': [
        'Sangamner City', 'Akole', 'Rahuri', 'Shrirampur', 'Nevasa',
        'Parner', 'Shevgaon', 'Pathardi', 'Rahata', 'Kopargaon',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmednagar Road', 'Nashik Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ahmednagar': [
        'Ahmednagar City', 'Sangamner', 'Kopargaon', 'Shrirampur', 'Rahuri',
        'Pathardi', 'Shevgaon', 'Parner', 'Nevasa', 'Akole',
        'Station Road', 'MG Road', 'Ring Road', 'Pune Road', 'Aurangabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Cantonment'
    ],
    'Wardha': [
        'Wardha City', 'Hinganghat', 'Pulgaon', 'Arvi', 'Seloo',
        'Deoli', 'Samudrapur', 'Ashti', 'Karanja', 'Talegaon',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Yavatmal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Yavatmal': [
        'Yavatmal City', 'Pusad', 'Umarkhed', 'Digras', 'Ghatanji',
        'Kalamb', 'Darwha', 'Maregaon', 'Ralegaon', 'Ner',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Wardha Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chandrapur': [
        'Chandrapur City', 'Warora', 'Ballarpur', 'Rajura', 'Mul',
        'Nagbhir', 'Bramhapuri', 'Gondpipri', 'Sindewahi', 'Korpana',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Gadchiroli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Gadchiroli': [
        'Gadchiroli City', 'Aheri', 'Sironcha', 'Chamorshi', 'Dhanora',
        'Kurkheda', 'Korchi', 'Desaiganj', 'Armori', 'Bhamragad',
        'Station Road', 'MG Road', 'Ring Road', 'Chandrapur Road', 'Nagpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bhandara': [
        'Bhandara City', 'Tumsar', 'Pauni', 'Lakhandur', 'Mohadi',
        'Sakoli', 'Lakhani', 'Tirora', 'Gondia', 'Deori',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Gondia Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Gondia': [
        'Gondia City', 'Tiroda', 'Goregaon', 'Amgaon', 'Salekasa',
        'Deori', 'Arjuni Morgaon', 'Sadak Arjuni', 'Tirora', 'Bhandara',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Bhandara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Washim': [
        'Washim City', 'Karanja', 'Risod', 'Mangrulpir', 'Malegaon',
        'Manora', 'Washim', 'Karanja', 'Risod', 'Mangrulpir',
        'Station Road', 'MG Road', 'Ring Road', 'Akola Road', 'Yavatmal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Buldhana': [
        'Buldhana City', 'Khamgaon', 'Jalgaon Jamod', 'Sindkhed Raja', 'Malkapur',
        'Chikhli', 'Nandura', 'Shegaon', 'Lonar', 'Deulgaon Raja',
        'Station Road', 'MG Road', 'Ring Road', 'Akola Road', 'Jalgaon Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Akola': [
        'Akola City', 'Murtijapur', 'Patur', 'Balapur', 'Telhara',
        'Akot', 'Barshitakli', 'Patur', 'Murtijapur', 'Balapur',
        'Station Road', 'MG Road', 'Ring Road', 'Nagpur Road', 'Amravati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Buldana': [
        'Buldhana City', 'Khamgaon', 'Jalgaon Jamod', 'Sindkhed Raja', 'Malkapur',
        'Chikhli', 'Nandura', 'Shegaon', 'Lonar', 'Deulgaon Raja',
        'Station Road', 'MG Road', 'Ring Road', 'Akola Road', 'Jalgaon Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
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
        'Simmakkal', 'Periyar', 'Teppakulam', 'Thirumangalam', 'Koodal Nagar',
        'Meenakshi Nagar', 'Vandiyur', 'Anaiyur', 'Kochadai', 'Arapalayam',
        'Chokkikulam', 'Karpagam Nagar', 'Shenoy Nagar', 'Tirupparankundram', 'Alagarkoil'
    ],
    'Tiruchirappalli': [
        'Trichy City', 'Srirangam', 'Woraiyur', 'Thillai Nagar', 'KK Nagar',
        'Bharathidasan Nagar', 'Gandhi Market', 'Cantonment', 'Golden Rock', 'Ponmalai',
        'Kailasapuram', 'Kattur', 'Kovilpatti', 'Manachanallur', 'Musiri',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Madurai Road'
    ],
    'Trichy': [
        'Trichy City', 'Srirangam', 'Woraiyur', 'Thillai Nagar', 'KK Nagar',
        'Bharathidasan Nagar', 'Gandhi Market', 'Cantonment', 'Golden Rock', 'Ponmalai',
        'Kailasapuram', 'Kattur', 'Kovilpatti', 'Manachanallur', 'Musiri',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Madurai Road'
    ],
    'Salem': [
        'Salem City', 'Hasthampatti', 'Kondalampatti', 'Suramangalam', 'Ammapet',
        'Fairlands', 'Gugai', 'Kannankurichi', 'Mettur', 'Omalur',
        'Attur', 'Edappadi', 'Rasipuram', 'Sankagiri', 'Yercaud',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Coimbatore Road'
    ],
    'Tirunelveli': [
        'Tirunelveli City', 'Palayamkottai', 'Thaatchanallur', 'Melapalayam', 'Tirunelveli Junction',
        'Nellai', 'Sankarankovil', 'Tenkasi', 'Ambasamudram', 'Cheranmahadevi',
        'Sivagiri', 'Shencottah', 'Kadayanallur', 'Valliyur', 'Radhapuram',
        'Station Road', 'MG Road', 'Ring Road', 'Nagercoil Road', 'Tuticorin Road'
    ],
    'Erode': [
        'Erode City', 'Bhavani', 'Gobichettipalayam', 'Sathyamangalam', 'Perundurai',
        'Kodumudi', 'Chennimalai', 'Modakurichi', 'Kangeyam', 'Anthiyur',
        'Station Road', 'MG Road', 'Ring Road', 'Coimbatore Road', 'Salem Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Vellore': [
        'Vellore City', 'Katpadi', 'Gudiyatham', 'Tirupattur', 'Ambur',
        'Vaniyambadi', 'Arakkonam', 'Ranipet', 'Wallajah', 'Arcot',
        'Cantonment', 'Sathuvachari', 'Krishnagiri Road', 'Bangalore Road', 'Chennai Road',
        'Station Road', 'MG Road', 'Ring Road', 'Katpadi Road'
    ],
    'Thoothukudi': [
        'Thoothukudi City', 'Tuticorin', 'Kovilpatti', 'Kayalpattinam', 'Tiruchendur',
        'Sathankulam', 'Vilathikulam', 'Ettayapuram', 'Ottapidaram', 'Vilathikulam',
        'Harbour', 'Port Area', 'Beach Road', 'Station Road', 'MG Road',
        'Ring Road', 'Tirunelveli Road', 'Madurai Road'
    ],
    'Tuticorin': [
        'Thoothukudi City', 'Tuticorin', 'Kovilpatti', 'Kayalpattinam', 'Tiruchendur',
        'Sathankulam', 'Vilathikulam', 'Ettayapuram', 'Ottapidaram', 'Vilathikulam',
        'Harbour', 'Port Area', 'Beach Road', 'Station Road', 'MG Road',
        'Ring Road', 'Tirunelveli Road', 'Madurai Road'
    ],
    'Dindigul': [
        'Dindigul City', 'Batlagundu', 'Nilakottai', 'Palani', 'Kodaikanal',
        'Oddanchatram', 'Vedasandur', 'Natham', 'Reddiyarchatram', 'Gujiliamparai',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Coimbatore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Thanjavur': [
        'Thanjavur City', 'Kumbakonam', 'Pattukkottai', 'Orathanadu', 'Thiruvaiyaru',
        'Thiruvidaimarudur', 'Papanasam', 'Budalur', 'Thirukattupalli', 'Ammapettai',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Kumbakonam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Tanjore': [
        'Thanjavur City', 'Kumbakonam', 'Pattukkottai', 'Orathanadu', 'Thiruvaiyaru',
        'Thiruvidaimarudur', 'Papanasam', 'Budalur', 'Thirukattupalli', 'Ammapettai',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Kumbakonam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kumbakonam': [
        'Kumbakonam City', 'Thanjavur', 'Pattukkottai', 'Orathanadu', 'Thiruvaiyaru',
        'Thiruvidaimarudur', 'Papanasam', 'Budalur', 'Thirukattupalli', 'Ammapettai',
        'Station Road', 'MG Road', 'Ring Road', 'Thanjavur Road', 'Mayiladuthurai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Tiruppur': [
        'Tiruppur City', 'Kangeyam', 'Dharapuram', 'Udumalpet', 'Palladam',
        'Avinashipalayam', 'Kangayam', 'Vellakoil', 'Mulanur', 'Uthukuli',
        'Station Road', 'MG Road', 'Ring Road', 'Coimbatore Road', 'Erode Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nagercoil': [
        'Nagercoil City', 'Kanyakumari', 'Kuzhithurai', 'Colachel', 'Kulasekaram',
        'Thuckalay', 'Thiruvattar', 'Marthandam', 'Pechiparai', 'Padmanabhapuram',
        'Station Road', 'MG Road', 'Ring Road', 'Kanyakumari Road', 'Tirunelveli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kanyakumari': [
        'Kanyakumari City', 'Nagercoil', 'Kuzhithurai', 'Colachel', 'Kulasekaram',
        'Thuckalay', 'Thiruvattar', 'Marthandam', 'Pechiparai', 'Padmanabhapuram',
        'Beach Road', 'Sunrise Point', 'Vivekananda Rock', 'Station Road', 'MG Road',
        'Ring Road', 'Nagercoil Road', 'Tirunelveli Road'
    ],
    'Karur': [
        'Karur City', 'Kulithalai', 'Krishnarayapuram', 'Kadavur', 'Aravakurichi',
        'Pugalur', 'Thanthoni', 'Thogaimalai', 'Kadavur', 'Kulithalai',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Dindigul Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Hosur': [
        'Hosur City', 'Denkanikottai', 'Krishnagiri', 'Bargur', 'Mathigiri',
        'Shoolagiri', 'Kelamangalam', 'Thally', 'Rayakottai', 'Bagalur',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road', 'Krishnagiri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Krishnagiri': [
        'Krishnagiri City', 'Hosur', 'Denkanikottai', 'Bargur', 'Mathigiri',
        'Shoolagiri', 'Kelamangalam', 'Thally', 'Rayakottai', 'Bagalur',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road', 'Salem Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Namakkal': [
        'Namakkal City', 'Rasipuram', 'Paramathi', 'Kumarapalayam', 'Tiruchengode',
        'Komarapalayam', 'Sendamangalam', 'Kolli Hills', 'Mohanur', 'Pallipalayam',
        'Station Road', 'MG Road', 'Ring Road', 'Salem Road', 'Erode Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Dharmapuri': [
        'Dharmapuri City', 'Hosur', 'Krishnagiri', 'Palacode', 'Pennagaram',
        'Pappireddipatti', 'Harur', 'Nallampalli', 'Karimangalam', 'Pappireddipatti',
        'Station Road', 'MG Road', 'Ring Road', 'Salem Road', 'Krishnagiri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Cuddalore': [
        'Cuddalore City', 'Chidambaram', 'Vriddhachalam', 'Kattumannarkoil', 'Kurinjipadi',
        'Panruti', 'Neyveli', 'Bhuvanagiri', 'Srimushnam', 'Kattumannarkoil',
        'Station Road', 'MG Road', 'Ring Road', 'Pondicherry Road', 'Chidambaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chidambaram': [
        'Chidambaram City', 'Cuddalore', 'Vriddhachalam', 'Kattumannarkoil', 'Kurinjipadi',
        'Panruti', 'Neyveli', 'Bhuvanagiri', 'Srimushnam', 'Kattumannarkoil',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Cuddalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Villupuram': [
        'Villupuram City', 'Tindivanam', 'Gingee', 'Kandamangalam', 'Vanur',
        'Marakkanam', 'Tindivanam', 'Gingee', 'Kandamangalam', 'Vanur',
        'Station Road', 'MG Road', 'Ring Road', 'Pondicherry Road', 'Cuddalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kanchipuram': [
        'Kanchipuram City', 'Sriperumbudur', 'Uthiramerur', 'Walajabad', 'Madurantakam',
        'Chengalpattu', 'Tambaram', 'Kanchipuram', 'Sriperumbudur', 'Uthiramerur',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Chengalpattu': [
        'Chengalpattu City', 'Kanchipuram', 'Sriperumbudur', 'Uthiramerur', 'Walajabad',
        'Madurantakam', 'Tambaram', 'Maraimalai Nagar', 'Singaperumal Koil', 'Kattankulathur',
        'Station Road', 'MG Road', 'Ring Road', 'Chennai Road', 'Kanchipuram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Pudukkottai': [
        'Pudukkottai City', 'Karaikudi', 'Devakottai', 'Arantangi', 'Ilayangudi',
        'Keeranur', 'Kulathur', 'Ponnamaravathi', 'Thirumayam', 'Viralimalai',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Karaikudi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Karaikudi': [
        'Karaikudi City', 'Pudukkottai', 'Devakottai', 'Arantangi', 'Ilayangudi',
        'Keeranur', 'Kulathur', 'Ponnamaravathi', 'Thirumayam', 'Viralimalai',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Pudukkottai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ramanathapuram': [
        'Ramanathapuram City', 'Rameswaram', 'Paramakudi', 'Mudukulathur', 'Tiruvadanai',
        'Kadaladi', 'Kamuthi', 'Tirupullani', 'Rameswaram', 'Paramakudi',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Rameswaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Rameswaram': [
        'Rameswaram City', 'Ramanathapuram', 'Paramakudi', 'Mudukulathur', 'Tiruvadanai',
        'Kadaladi', 'Kamuthi', 'Tirupullani', 'Rameswaram', 'Paramakudi',
        'Temple Area', 'Beach Road', 'Station Road', 'MG Road', 'Ramanathapuram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Sivaganga': [
        'Sivaganga City', 'Karaikudi', 'Devakottai', 'Ilayangudi', 'Manamadurai',
        'Thirupuvanam', 'Sivaganga', 'Karaikudi', 'Devakottai', 'Ilayangudi',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Ramanathapuram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Theni': [
        'Theni City', 'Bodinayakkanur', 'Cumbum', 'Periyakulam', 'Uthamapalayam',
        'Andipatti', 'Theni Allinagaram', 'Bodinayakkanur', 'Cumbum', 'Periyakulam',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Dindigul Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Virudhunagar': [
        'Virudhunagar City', 'Sivakasi', 'Rajapalayam', 'Srivilliputhur', 'Aruppukottai',
        'Sattur', 'Tiruchuli', 'Vembakottai', 'Watrap', 'Narikkudi',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Tuticorin Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Sivakasi': [
        'Sivakasi City', 'Virudhunagar', 'Rajapalayam', 'Srivilliputhur', 'Aruppukottai',
        'Sattur', 'Tiruchuli', 'Vembakottai', 'Watrap', 'Narikkudi',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Virudhunagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Rajapalayam': [
        'Rajapalayam City', 'Virudhunagar', 'Sivakasi', 'Srivilliputhur', 'Aruppukottai',
        'Sattur', 'Tiruchuli', 'Vembakottai', 'Watrap', 'Narikkudi',
        'Station Road', 'MG Road', 'Ring Road', 'Madurai Road', 'Sivakasi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ariyalur': [
        'Ariyalur City', 'Jayankondam', 'Sendurai', 'Udayarpalayam', 'Andimadam',
        'Ariyalur', 'Jayankondam', 'Sendurai', 'Udayarpalayam', 'Andimadam',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Perambalur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Perambalur': [
        'Perambalur City', 'Ariyalur', 'Jayankondam', 'Sendurai', 'Udayarpalayam',
        'Andimadam', 'Ariyalur', 'Jayankondam', 'Sendurai', 'Udayarpalayam',
        'Station Road', 'MG Road', 'Ring Road', 'Trichy Road', 'Ariyalur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nagapattinam': [
        'Nagapattinam City', 'Vedaranyam', 'Thirukkuvalai', 'Kilvelur', 'Thalainayar',
        'Sirkazhi', 'Mayiladuthurai', 'Karaikal', 'Nagapattinam', 'Vedaranyam',
        'Station Road', 'MG Road', 'Ring Road', 'Karaikal Road', 'Mayiladuthurai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mayiladuthurai': [
        'Mayiladuthurai City', 'Nagapattinam', 'Vedaranyam', 'Thirukkuvalai', 'Kilvelur',
        'Thalainayar', 'Sirkazhi', 'Karaikal', 'Nagapattinam', 'Vedaranyam',
        'Station Road', 'MG Road', 'Ring Road', 'Kumbakonam Road', 'Nagapattinam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Thiruvarur': [
        'Thiruvarur City', 'Nagapattinam', 'Mannargudi', 'Thiruthuraipoondi', 'Nannilam',
        'Kodavasal', 'Valangaiman', 'Needamangalam', 'Thiruvarur', 'Mannargudi',
        'Station Road', 'MG Road', 'Ring Road', 'Nagapattinam Road', 'Thanjavur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mannargudi': [
        'Mannargudi City', 'Thiruvarur', 'Nagapattinam', 'Thiruthuraipoondi', 'Nannilam',
        'Kodavasal', 'Valangaiman', 'Needamangalam', 'Thiruvarur', 'Nagapattinam',
        'Station Road', 'MG Road', 'Ring Road', 'Thanjavur Road', 'Thiruvarur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Pollachi': [
        'Pollachi City', 'Coimbatore', 'Udumalpet', 'Valparai', 'Anamalai',
        'Topslip', 'Aliyar', 'Pollachi', 'Udumalpet', 'Valparai',
        'Station Road', 'MG Road', 'Ring Road', 'Coimbatore Road', 'Palani Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ooty': [
        'Ooty City', 'Udhagamandalam', 'Coonoor', 'Kotagiri', 'Gudalur',
        'Avalanche', 'Emerald', 'Kundah', 'Mudumalai', 'Pykara',
        'Station Road', 'MG Road', 'Ring Road', 'Coonoor Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Udhagamandalam': [
        'Ooty City', 'Udhagamandalam', 'Coonoor', 'Kotagiri', 'Gudalur',
        'Avalanche', 'Emerald', 'Kundah', 'Mudumalai', 'Pykara',
        'Station Road', 'MG Road', 'Ring Road', 'Coonoor Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Coonoor': [
        'Coonoor City', 'Ooty', 'Udhagamandalam', 'Kotagiri', 'Gudalur',
        'Avalanche', 'Emerald', 'Kundah', 'Mudumalai', 'Pykara',
        'Station Road', 'MG Road', 'Ring Road', 'Ooty Road', 'Mysore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kodaikanal': [
        'Kodaikanal City', 'Palani', 'Dindigul', 'Batlagundu', 'Vathalagundu',
        'Poombarai', 'Berijam', 'Kodaikanal', 'Palani', 'Dindigul',
        'Lake Area', 'Station Road', 'MG Road', 'Ring Road', 'Palani Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Yercaud': [
        'Yercaud City', 'Salem', 'Attur', 'Omalur', 'Mettur',
        'Yercaud Hills', 'Salem', 'Attur', 'Omalur', 'Mettur',
        'Station Road', 'MG Road', 'Ring Road', 'Salem Road', 'Attur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
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
        'Hanamkonda', 'Kazipet', 'Subedari', 'Enumamula', 'Narsampet',
        'Warangal City', 'Kakatiya University', 'Station Road', 'MG Road', 'Ring Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Kazipet Road'
    ],
    'Nizamabad': [
        'Nizamabad City', 'Armoor', 'Bodhan', 'Kamareddy', 'Yellareddy',
        'Banswada', 'Bichkunda', 'Birkur', 'Dichpally', 'Domakonda',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Kamareddy Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Karimnagar': [
        'Karimnagar City', 'Jagtial', 'Peddapalli', 'Manthani', 'Sircilla',
        'Huzurabad', 'Vemulawada', 'Sircilla', 'Jagtial', 'Peddapalli',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Warangal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Ramagundam': [
        'Ramagundam City', 'Mancherial', 'Bellampalli', 'Mandamarri', 'Srirampur',
        'Peddapalli', 'Manthani', 'Ramagundam', 'Mancherial', 'Bellampalli',
        'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Khammam': [
        'Khammam City', 'Kothagudem', 'Bhadrachalam', 'Yellandu', 'Paloncha',
        'Madhira', 'Sathupalli', 'Wyra', 'Enkoor', 'Kallur',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Vijayawada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mahbubnagar': [
        'Mahbubnagar City', 'Gadwal', 'Wanaparthy', 'Narayanpet', 'Kodangal',
        'Achampet', 'Alampur', 'Kollapur', 'Makthal', 'Nagarkurnool',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nalgonda': [
        'Nalgonda City', 'Suryapet', 'Miryalaguda', 'Bhongir', 'Devarakonda',
        'Nakrekal', 'Choutuppal', 'Mothkur', 'Huzurnagar', 'Chityal',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Vijayawada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Suryapet': [
        'Suryapet City', 'Nalgonda', 'Miryalaguda', 'Bhongir', 'Devarakonda',
        'Nakrekal', 'Choutuppal', 'Mothkur', 'Huzurnagar', 'Chityal',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Nalgonda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Medak': [
        'Medak City', 'Siddipet', 'Zahirabad', 'Gajwel', 'Narsapur',
        'Sangareddy', 'Toopran', 'Narayankhed', 'Shankarampet', 'Andole',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Siddipet Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Siddipet': [
        'Siddipet City', 'Medak', 'Zahirabad', 'Gajwel', 'Narsapur',
        'Sangareddy', 'Toopran', 'Narayankhed', 'Shankarampet', 'Andole',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Medak Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Sangareddy': [
        'Sangareddy City', 'Medak', 'Siddipet', 'Zahirabad', 'Gajwel',
        'Narsapur', 'Toopran', 'Narayankhed', 'Shankarampet', 'Andole',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Medak Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Adilabad': [
        'Adilabad City', 'Nirmal', 'Mancherial', 'Bellampalli', 'Asifabad',
        'Utnoor', 'Narnoor', 'Indravelli', 'Bazarhathnoor', 'Ichoda',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Nirmal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nirmal': [
        'Nirmal City', 'Adilabad', 'Mancherial', 'Bellampalli', 'Asifabad',
        'Utnoor', 'Narnoor', 'Indravelli', 'Bazarhathnoor', 'Ichoda',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Adilabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mancherial': [
        'Mancherial City', 'Adilabad', 'Nirmal', 'Bellampalli', 'Asifabad',
        'Utnoor', 'Narnoor', 'Indravelli', 'Bazarhathnoor', 'Ichoda',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Adilabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Jagtial': [
        'Jagtial City', 'Karimnagar', 'Peddapalli', 'Manthani', 'Sircilla',
        'Huzurabad', 'Vemulawada', 'Sircilla', 'Karimnagar', 'Peddapalli',
        'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Peddapalli': [
        'Peddapalli City', 'Karimnagar', 'Jagtial', 'Manthani', 'Sircilla',
        'Huzurabad', 'Vemulawada', 'Sircilla', 'Jagtial', 'Karimnagar',
        'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road', 'Ramagundam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kamareddy': [
        'Kamareddy City', 'Nizamabad', 'Armoor', 'Bodhan', 'Yellareddy',
        'Banswada', 'Bichkunda', 'Birkur', 'Dichpally', 'Domakonda',
        'Station Road', 'MG Road', 'Ring Road', 'Nizamabad Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bhongir': [
        'Bhongir City', 'Nalgonda', 'Suryapet', 'Miryalaguda', 'Devarakonda',
        'Nakrekal', 'Choutuppal', 'Mothkur', 'Huzurnagar', 'Chityal',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Nalgonda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Miryalaguda': [
        'Miryalaguda City', 'Nalgonda', 'Suryapet', 'Bhongir', 'Devarakonda',
        'Nakrekal', 'Choutuppal', 'Mothkur', 'Huzurnagar', 'Chityal',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Nalgonda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Kothagudem': [
        'Kothagudem City', 'Khammam', 'Bhadrachalam', 'Yellandu', 'Paloncha',
        'Madhira', 'Sathupalli', 'Wyra', 'Enkoor', 'Kallur',
        'Station Road', 'MG Road', 'Ring Road', 'Khammam Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bhadrachalam': [
        'Bhadrachalam City', 'Khammam', 'Kothagudem', 'Yellandu', 'Paloncha',
        'Madhira', 'Sathupalli', 'Wyra', 'Enkoor', 'Kallur',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Khammam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Gadwal': [
        'Gadwal City', 'Mahbubnagar', 'Wanaparthy', 'Narayanpet', 'Kodangal',
        'Achampet', 'Alampur', 'Kollapur', 'Makthal', 'Nagarkurnool',
        'Station Road', 'MG Road', 'Ring Road', 'Mahbubnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Wanaparthy': [
        'Wanaparthy City', 'Mahbubnagar', 'Gadwal', 'Narayanpet', 'Kodangal',
        'Achampet', 'Alampur', 'Kollapur', 'Makthal', 'Nagarkurnool',
        'Station Road', 'MG Road', 'Ring Road', 'Mahbubnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Narayanpet': [
        'Narayanpet City', 'Mahbubnagar', 'Gadwal', 'Wanaparthy', 'Kodangal',
        'Achampet', 'Alampur', 'Kollapur', 'Makthal', 'Nagarkurnool',
        'Station Road', 'MG Road', 'Ring Road', 'Mahbubnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Nagarkurnool': [
        'Nagarkurnool City', 'Mahbubnagar', 'Gadwal', 'Wanaparthy', 'Narayanpet',
        'Achampet', 'Alampur', 'Kollapur', 'Makthal', 'Kodangal',
        'Station Road', 'MG Road', 'Ring Road', 'Mahbubnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Jangaon': [
        'Jangaon City', 'Warangal', 'Hanamkonda', 'Kazipet', 'Subedari',
        'Enumamula', 'Narsampet', 'Warangal', 'Hanamkonda', 'Kazipet',
        'Station Road', 'MG Road', 'Ring Road', 'Warangal Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Mahabubabad': [
        'Mahabubabad City', 'Warangal', 'Khammam', 'Kothagudem', 'Bhadrachalam',
        'Yellandu', 'Paloncha', 'Madhira', 'Sathupalli', 'Wyra',
        'Station Road', 'MG Road', 'Ring Road', 'Warangal Road', 'Khammam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Vikarabad': [
        'Vikarabad City', 'Hyderabad', 'Ranga Reddy', 'Tandur', 'Pargi',
        'Dharur', 'Kodangal', 'Mominpet', 'Bantwaram', 'Pargi',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Ranga Reddy Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Sircilla': [
        'Sircilla City', 'Karimnagar', 'Jagtial', 'Peddapalli', 'Manthani',
        'Huzurabad', 'Vemulawada', 'Karimnagar', 'Jagtial', 'Peddapalli',
        'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Huzurabad': [
        'Huzurabad City', 'Karimnagar', 'Jagtial', 'Peddapalli', 'Manthani',
        'Sircilla', 'Vemulawada', 'Karimnagar', 'Jagtial', 'Peddapalli',
        'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Vemulawada': [
        'Vemulawada City', 'Karimnagar', 'Jagtial', 'Peddapalli', 'Manthani',
        'Sircilla', 'Huzurabad', 'Karimnagar', 'Jagtial', 'Peddapalli',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Karimnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Armoor': [
        'Armoor City', 'Nizamabad', 'Kamareddy', 'Bodhan', 'Yellareddy',
        'Banswada', 'Bichkunda', 'Birkur', 'Dichpally', 'Domakonda',
        'Station Road', 'MG Road', 'Ring Road', 'Nizamabad Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Bodhan': [
        'Bodhan City', 'Nizamabad', 'Kamareddy', 'Armoor', 'Yellareddy',
        'Banswada', 'Bichkunda', 'Birkur', 'Dichpally', 'Domakonda',
        'Station Road', 'MG Road', 'Ring Road', 'Nizamabad Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
    ],
    'Secunderabad': [
        'Secunderabad City', 'Hyderabad', 'Begumpet', 'Paradise', 'Malkajgiri',
        'Tarnaka', 'Uppal', 'Nagole', 'LB Nagar', 'Dilsukhnagar',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Begumpet Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar'
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
    'Greater Noida': [
        'Greater Noida West', 'Greater Noida East', 'Knowledge Park', 'Alpha', 'Beta',
        'Gamma', 'Delta', 'Eta', 'Theta', 'Zeta',
        'Sector Alpha', 'Sector Beta', 'Sector Gamma', 'Sector Delta', 'Sector Eta',
        'Sector Theta', 'Sector Zeta', 'Knowledge Park I', 'Knowledge Park II', 'Knowledge Park III',
        'Knowledge Park IV', 'Knowledge Park V', 'Tech Zone', 'Eco Tech Village', 'Gaur City',
        'Noida Extension', 'Yamuna Expressway', 'Noida-Greater Noida Expressway', 'Dadri Road', 'Jewar Road'
    ],
    'Faridabad': [
        'Faridabad City', 'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4',
        'Sector 5', 'Sector 6', 'Sector 7', 'Sector 8', 'Sector 9',
        'Sector 10', 'Sector 11', 'Sector 12', 'Sector 13', 'Sector 14',
        'Sector 15', 'Sector 16', 'Sector 17', 'Sector 18', 'Sector 19',
        'Sector 20', 'Sector 21', 'Sector 22', 'Sector 23', 'Sector 24',
        'Sector 25', 'Sector 26', 'Sector 27', 'Sector 28', 'Sector 29',
        'Sector 30', 'Sector 31', 'Sector 32', 'Sector 33', 'Sector 34',
        'Sector 35', 'Sector 36', 'Sector 37', 'Sector 38', 'Sector 39',
        'Sector 40', 'Sector 41', 'Sector 42', 'Sector 43', 'Sector 44',
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
        'Sector 115', 'Ballabhgarh', 'Palwal', 'Hathin', 'Hodal',
        'Tigaon', 'Badkhal', 'Ankhir', 'Aravali Golf Course', 'Crown Plaza',
        'Greenfield Colony', 'Neelam Bata Road', 'Mathura Road', 'Agra Canal Road', 'NH-2'
    ],
    'Ghaziabad': [
        'Ghaziabad City', 'Indirapuram', 'Vaishali', 'Kaushambi', 'Crossings Republik',
        'Raj Nagar Extension', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Muradnagar', 'Dasna', 'Bhojpur', 'Vijay Nagar', 'Shalimar Garden',
        'Rajendra Nagar', 'Kavi Nagar', 'Sanjay Nagar', 'Shyam Park', 'Shastri Nagar',
        'Nehru Nagar', 'Govindpuram', 'Surya Nagar', 'Pratap Vihar', 'Sihani Gate',
        'Old Ghaziabad', 'New Ghaziabad', 'Lal Kuan', 'Mohan Nagar', 'Shyam Park Extension',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
    ],
    'Sonipat': [
        'Sonipat City', 'Murthal', 'Gohana', 'Ganaur', 'Kharkhoda',
        'Rai', 'Kundli', 'Atlas', 'Bahalgarh', 'Rathdhana',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Panipat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Panipat': [
        'Panipat City', 'Samalkha', 'Israna', 'Madlauda', 'Bapoli',
        'Asan Kalan', 'Naultha', 'Panipat', 'Samalkha', 'Israna',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Karnal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Karnal': [
        'Karnal City', 'Assandh', 'Gharaunda', 'Indri', 'Nissing',
        'Nilokheri', 'Kunjpura', 'Karnal', 'Assandh', 'Gharaunda',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Panipat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rohtak': [
        'Rohtak City', 'Meham', 'Kalanaur', 'Sampla', 'Lakhan Majra',
        'Beri', 'Jhajjar', 'Bahadurgarh', 'Rohtak', 'Meham',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Hisar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rewari': [
        'Rewari City', 'Bawal', 'Dharuhera', 'Kosli', 'Nahar',
        'Pali', 'Jatusana', 'Rewari', 'Bawal', 'Dharuhera',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Gurgaon Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Meerut': [
        'Meerut City', 'Modipuram', 'Sardhana', 'Mawana', 'Kharkhoda',
        'Sardhana', 'Mawana', 'Kharkhoda', 'Modipuram', 'Sardhana',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Ghaziabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bulandshahr': [
        'Bulandshahr City', 'Khurja', 'Sikandrabad', 'Anupshahr', 'Debai',
        'Shikarpur', 'Jahangirabad', 'Bulandshahr', 'Khurja', 'Sikandrabad',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Aligarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Alwar': [
        'Alwar City', 'Bhiwadi', 'Behror', 'Tijara', 'Kishangarh',
        'Rajgarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Jaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhiwadi': [
        'Bhiwadi City', 'Alwar', 'Behror', 'Tijara', 'Kishangarh',
        'Rajgarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Behror',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Alwar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Palwal': [
        'Palwal City', 'Hodal', 'Hathin', 'Hassanpur', 'Kosi',
        'Mandkola', 'Palwal', 'Hodal', 'Hathin', 'Hassanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Mathura Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ballabhgarh': [
        'Ballabhgarh City', 'Faridabad', 'Palwal', 'Hodal', 'Hathin',
        'Hassanpur', 'Kosi', 'Mandkola', 'Faridabad', 'Palwal',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Faridabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bahadurgarh': [
        'Bahadurgarh City', 'Rohtak', 'Jhajjar', 'Sampla', 'Lakhan Majra',
        'Beri', 'Meham', 'Kalanaur', 'Rohtak', 'Jhajjar',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Rohtak Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hapur': [
        'Hapur City', 'Bulandshahr', 'Ghaziabad', 'Meerut', 'Modinagar',
        'Garhmukteshwar', 'Dabur', 'Hapur', 'Bulandshahr', 'Ghaziabad',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Meerut Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Modinagar': [
        'Modinagar City', 'Ghaziabad', 'Hapur', 'Bulandshahr', 'Meerut',
        'Garhmukteshwar', 'Dabur', 'Ghaziabad', 'Hapur', 'Bulandshahr',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Ghaziabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Muzaffarnagar': [
        'Muzaffarnagar City', 'Shamli', 'Baghpat', 'Kairana', 'Budhana',
        'Jansath', 'Khatauli', 'Muzaffarnagar', 'Shamli', 'Baghpat',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Meerut Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Baghpat': [
        'Baghpat City', 'Baraut', 'Khekra', 'Chhaprauli', 'Binauli',
        'Nangloi', 'Baraut', 'Khekra', 'Chhaprauli', 'Binauli',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Meerut Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Shamli': [
        'Shamli City', 'Muzaffarnagar', 'Baghpat', 'Kairana', 'Budhana',
        'Jansath', 'Khatauli', 'Muzaffarnagar', 'Baghpat', 'Kairana',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Muzaffarnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jhajjar': [
        'Jhajjar City', 'Rohtak', 'Bahadurgarh', 'Sampla', 'Lakhan Majra',
        'Beri', 'Meham', 'Kalanaur', 'Rohtak', 'Bahadurgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Rohtak Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hisar': [
        'Hisar City', 'Bhiwani', 'Fatehabad', 'Sirsa', 'Tohana',
        'Adampur', 'Barwala', 'Hisar', 'Bhiwani', 'Fatehabad',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Rohtak Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Yamunanagar': [
        'Yamunanagar City', 'Jagadhri', 'Chhachhrauli', 'Bilaspur', 'Radaur',
        'Mustafabad', 'Sadhaura', 'Yamunanagar', 'Jagadhri', 'Chhachhrauli',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Ambala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ambala': [
        'Ambala City', 'Ambala Cantonment', 'Ambala City', 'Barara', 'Naraingarh',
        'Shahzadpur', 'Mullana', 'Ambala', 'Ambala Cantonment', 'Barara',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Chandigarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Indirapuram': [
        'Indirapuram City', 'Ghaziabad', 'Vaishali', 'Kaushambi', 'Crossings Republik',
        'Raj Nagar Extension', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Ahinsa Khand', 'Pratap Vihar', 'Surya Nagar', 'Shyam Park', 'Nehru Nagar',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
    ],
    'Vaishali': [
        'Vaishali City', 'Ghaziabad', 'Indirapuram', 'Kaushambi', 'Crossings Republik',
        'Raj Nagar Extension', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Ahinsa Khand', 'Pratap Vihar', 'Surya Nagar', 'Shyam Park', 'Nehru Nagar',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
    ],
    'Kaushambi': [
        'Kaushambi City', 'Ghaziabad', 'Indirapuram', 'Vaishali', 'Crossings Republik',
        'Raj Nagar Extension', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Ahinsa Khand', 'Pratap Vihar', 'Surya Nagar', 'Shyam Park', 'Nehru Nagar',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
    ],
    'Crossings Republik': [
        'Crossings Republik City', 'Ghaziabad', 'Indirapuram', 'Vaishali', 'Kaushambi',
        'Raj Nagar Extension', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Ahinsa Khand', 'Pratap Vihar', 'Surya Nagar', 'Shyam Park', 'Nehru Nagar',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
    ],
    'Raj Nagar Extension': [
        'Raj Nagar Extension City', 'Ghaziabad', 'Indirapuram', 'Vaishali', 'Kaushambi',
        'Crossings Republik', 'Raj Nagar', 'Sahibabad', 'Loni', 'Modi Nagar',
        'Ahinsa Khand', 'Pratap Vihar', 'Surya Nagar', 'Shyam Park', 'Nehru Nagar',
        'NH-24', 'Meerut Road', 'Hapur Road', 'Bulandshahr Road', 'Delhi Road'
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
        'Gotri', 'Waghodia', 'Harni', 'Karelibaug', 'Tandalja',
        'Manjalpur', 'Subhanpura', 'Sama', 'Chhani', 'Tarsali',
        'Karelibaug', 'New VIP Road', 'Old Padra Road', 'Race Course', 'Ellora Park'
    ],
    'Rajkot': [
        'Rajkot City', 'Gondal', 'Jetpur', 'Upleta', 'Dhoraji',
        'Jamkandorna', 'Lodhika', 'Maliya', 'Morbi', 'Wankaner',
        'Kalavad Road', '150 Feet Ring Road', 'University Road', 'Gondal Road', 'Jetpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhavnagar': [
        'Bhavnagar City', 'Palitana', 'Mahuva', 'Talaja', 'Gariadhar',
        'Sihor', 'Vallabhipur', 'Ghogha', 'Botad', 'Umrala',
        'Station Road', 'MG Road', 'Ring Road', 'Palitana Road', 'Mahuva Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jamnagar': [
        'Jamnagar City', 'Dwarka', 'Porbandar', 'Khambhalia', 'Lalpur',
        'Dhrol', 'Jodiya', 'Kalavad', 'Bhanvad', 'Okha',
        'Station Road', 'MG Road', 'Ring Road', 'Dwarka Road', 'Porbandar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gandhinagar': [
        'Gandhinagar City', 'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4',
        'Sector 5', 'Sector 6', 'Sector 7', 'Sector 8', 'Sector 9',
        'Sector 10', 'Sector 11', 'Sector 12', 'Sector 13', 'Sector 14',
        'Sector 15', 'Sector 16', 'Sector 17', 'Sector 18', 'Sector 19',
        'Sector 20', 'Sector 21', 'Sector 22', 'Sector 23', 'Sector 24',
        'Sector 25', 'Sector 26', 'Sector 27', 'Sector 28', 'Sector 29',
        'Sector 30', 'Ahmedabad Road', 'Koba', 'Infocity', 'GIFT City'
    ],
    'Anand': [
        'Anand City', 'Vallabh Vidyanagar', 'Karamsad', 'Borsad', 'Petlad',
        'Sojitra', 'Umreth', 'Anklav', 'Tarapur', 'Khambhat',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Ahmedabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bharuch': [
        'Bharuch City', 'Ankleshwar', 'Jambusar', 'Dahej', 'Jhagadia',
        'Amod', 'Hansot', 'Vagra', 'Valia', 'Zadeshwar',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Vadodara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gandhidham': [
        'Gandhidham City', 'Kandla', 'Adipur', 'Anjar', 'Bhuj',
        'Mandvi', 'Mundra', 'Nakhatrana', 'Rapar', 'Bhachau',
        'Station Road', 'MG Road', 'Ring Road', 'Kandla Road', 'Bhuj Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhuj': [
        'Bhuj City', 'Gandhidham', 'Kandla', 'Adipur', 'Anjar',
        'Mandvi', 'Mundra', 'Nakhatrana', 'Rapar', 'Bhachau',
        'Station Road', 'MG Road', 'Ring Road', 'Gandhidham Road', 'Kandla Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Junagadh': [
        'Junagadh City', 'Veraval', 'Somnath', 'Keshod', 'Mangrol',
        'Visavadar', 'Manavadar', 'Kodinar', 'Una', 'Talala',
        'Station Road', 'MG Road', 'Ring Road', 'Veraval Road', 'Somnath Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Veraval': [
        'Veraval City', 'Junagadh', 'Somnath', 'Keshod', 'Mangrol',
        'Visavadar', 'Manavadar', 'Kodinar', 'Una', 'Talala',
        'Station Road', 'MG Road', 'Ring Road', 'Junagadh Road', 'Somnath Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Somnath': [
        'Somnath City', 'Veraval', 'Junagadh', 'Keshod', 'Mangrol',
        'Visavadar', 'Manavadar', 'Kodinar', 'Una', 'Talala',
        'Temple Area', 'Beach Road', 'Station Road', 'MG Road', 'Veraval Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Porbandar': [
        'Porbandar City', 'Dwarka', 'Jamnagar', 'Kutiyana', 'Ranavav',
        'Bhanvad', 'Kalyanpur', 'Porbandar', 'Dwarka', 'Jamnagar',
        'Station Road', 'MG Road', 'Ring Road', 'Dwarka Road', 'Jamnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dwarka': [
        'Dwarka City', 'Porbandar', 'Jamnagar', 'Kutiyana', 'Ranavav',
        'Bhanvad', 'Kalyanpur', 'Porbandar', 'Jamnagar', 'Kutiyana',
        'Temple Area', 'Beach Road', 'Station Road', 'MG Road', 'Porbandar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mehsana': [
        'Mehsana City', 'Visnagar', 'Kadi', 'Unjha', 'Becharaji',
        'Vadnagar', 'Kheralu', 'Satlasana', 'Vijapur', 'Mansa',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Palanpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Palanpur': [
        'Palanpur City', 'Banaskantha', 'Deesa', 'Danta', 'Kankrej',
        'Tharad', 'Vadgam', 'Vav', 'Dhanera', 'Deodar',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Mehsana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Patan': [
        'Patan City', 'Siddhpur', 'Radhanpur', 'Chanasma', 'Santalpur',
        'Sami', 'Harij', 'Sarasvati', 'Sidhpur', 'Radhanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Mehsana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Surendranagar': [
        'Surendranagar City', 'Wadhwan', 'Dhrangadhra', 'Limbdi', 'Chotila',
        'Sayla', 'Muli', 'Lakhtar', 'Chuda', 'Dasada',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Rajkot Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Morbi': [
        'Morbi City', 'Rajkot', 'Wankaner', 'Maliya', 'Halvad',
        'Dhrangadhra', 'Limbdi', 'Chotila', 'Sayla', 'Muli',
        'Station Road', 'MG Road', 'Ring Road', 'Rajkot Road', 'Wankaner Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nadiad': [
        'Nadiad City', 'Anand', 'Petlad', 'Borsad', 'Karamsad',
        'Umreth', 'Sojitra', 'Anklav', 'Tarapur', 'Khambhat',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Anand Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Navsari': [
        'Navsari City', 'Valsad', 'Bilimora', 'Gandevi', 'Chikhli',
        'Jalalpore', 'Dandi', 'Vansda', 'Dharampur', 'Pardi',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Valsad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Valsad': [
        'Valsad City', 'Navsari', 'Bilimora', 'Gandevi', 'Chikhli',
        'Jalalpore', 'Dandi', 'Vansda', 'Dharampur', 'Pardi',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Navsari Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Vapi': [
        'Vapi City', 'Valsad', 'Navsari', 'Bilimora', 'Gandevi',
        'Chikhli', 'Jalalpore', 'Dandi', 'Vansda', 'Dharampur',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Valsad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dahod': [
        'Dahod City', 'Godhra', 'Limkheda', 'Jhalod', 'Fatepura',
        'Garbada', 'Devgadh Baria', 'Santrampur', 'Kadana', 'Khanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Godhra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Godhra': [
        'Godhra City', 'Dahod', 'Limkheda', 'Jhalod', 'Fatepura',
        'Garbada', 'Devgadh Baria', 'Santrampur', 'Kadana', 'Khanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Dahod Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sabarkantha': [
        'Himmatnagar City', 'Idar', 'Khedbrahma', 'Vijaynagar', 'Bhiloda',
        'Modasa', 'Malpur', 'Prantij', 'Talod', 'Bayad',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Udaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Himmatnagar': [
        'Himmatnagar City', 'Idar', 'Khedbrahma', 'Vijaynagar', 'Bhiloda',
        'Modasa', 'Malpur', 'Prantij', 'Talod', 'Bayad',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Udaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Amreli': [
        'Amreli City', 'Rajula', 'Babra', 'Lathi', 'Savar Kundla',
        'Dhari', 'Jafrabad', 'Kunkavav', 'Bagasara', 'Kodinar',
        'Station Road', 'MG Road', 'Ring Road', 'Rajkot Road', 'Bhavnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Botad': [
        'Botad City', 'Bhavnagar', 'Gariadhar', 'Talaja', 'Mahuva',
        'Palitana', 'Sihor', 'Vallabhipur', 'Ghogha', 'Umrala',
        'Station Road', 'MG Road', 'Ring Road', 'Bhavnagar Road', 'Ahmedabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dang': [
        'Ahwa City', 'Dang', 'Subir', 'Waghai', 'Saputara',
        'Purna', 'Dang', 'Subir', 'Waghai', 'Saputara',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Valsad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ahwa': [
        'Ahwa City', 'Dang', 'Subir', 'Waghai', 'Saputara',
        'Purna', 'Dang', 'Subir', 'Waghai', 'Saputara',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Valsad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kutch': [
        'Bhuj City', 'Gandhidham', 'Kandla', 'Adipur', 'Anjar',
        'Mandvi', 'Mundra', 'Nakhatrana', 'Rapar', 'Bhachau',
        'Station Road', 'MG Road', 'Ring Road', 'Gandhidham Road', 'Kandla Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ankleshwar': [
        'Ankleshwar City', 'Bharuch', 'Jambusar', 'Dahej', 'Jhagadia',
        'Amod', 'Hansot', 'Vagra', 'Valia', 'Zadeshwar',
        'Station Road', 'MG Road', 'Ring Road', 'Bharuch Road', 'Surat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kheda': [
        'Nadiad City', 'Anand', 'Petlad', 'Borsad', 'Karamsad',
        'Umreth', 'Sojitra', 'Anklav', 'Tarapur', 'Khambhat',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Anand Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tapi': [
        'Vyara City', 'Songadh', 'Nizar', 'Uchhal', 'Dolvan',
        'Valod', 'Kukarmunda', 'Vyara', 'Songadh', 'Nizar',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Navsari Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Vyara': [
        'Vyara City', 'Songadh', 'Nizar', 'Uchhal', 'Dolvan',
        'Valod', 'Kukarmunda', 'Vyara', 'Songadh', 'Nizar',
        'Station Road', 'MG Road', 'Ring Road', 'Surat Road', 'Navsari Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Aravalli': [
        'Modasa City', 'Bayad', 'Malpur', 'Bhiloda', 'Dhansura',
        'Meghraj', 'Bhiloda', 'Malpur', 'Prantij', 'Talod',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Himmatnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Modasa': [
        'Modasa City', 'Bayad', 'Malpur', 'Bhiloda', 'Dhansura',
        'Meghraj', 'Bhiloda', 'Malpur', 'Prantij', 'Talod',
        'Station Road', 'MG Road', 'Ring Road', 'Ahmedabad Road', 'Himmatnagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mahisagar': [
        'Lunavada City', 'Santrampur', 'Kadana', 'Khanpur', 'Balasinor',
        'Virpur', 'Lunavada', 'Santrampur', 'Kadana', 'Khanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Godhra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Lunavada': [
        'Lunavada City', 'Santrampur', 'Kadana', 'Khanpur', 'Balasinor',
        'Virpur', 'Lunavada', 'Santrampur', 'Kadana', 'Khanpur',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Godhra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chhota Udaipur': [
        'Chhota Udaipur City', 'Pavagadh', 'Halol', 'Kalol', 'Dabhoi',
        'Sankheda', 'Kavant', 'Nasvadi', 'Chhota Udaipur', 'Pavagadh',
        'Station Road', 'MG Road', 'Ring Road', 'Vadodara Road', 'Ahmedabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Devbhumi Dwarka': [
        'Khambhalia City', 'Dwarka', 'Porbandar', 'Jamnagar', 'Okha',
        'Kalyanpur', 'Bhanvad', 'Khambhalia', 'Dwarka', 'Porbandar',
        'Station Road', 'MG Road', 'Ring Road', 'Jamnagar Road', 'Dwarka Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Khambhalia': [
        'Khambhalia City', 'Dwarka', 'Porbandar', 'Jamnagar', 'Okha',
        'Kalyanpur', 'Bhanvad', 'Khambhalia', 'Dwarka', 'Porbandar',
        'Station Road', 'MG Road', 'Ring Road', 'Jamnagar Road', 'Dwarka Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    
    # West Bengal
    'Kolkata': [
        'Salt Lake', 'New Town', 'Rajarhat', 'Howrah', 'Dum Dum',
        'Barasat', 'Kalyani', 'Bidhannagar', 'Behala', 'Alipore',
        'Park Street', 'Esplanade', 'BBD Bagh', 'Dalhousie', 'Chowringhee',
        'Tollygunge', 'Garia', 'Jadavpur', 'Santoshpur', 'Bansdroni',
        'Narendrapur', 'Sonarpur', 'Baruipur', 'Diamond Harbour', 'Kakdwip',
        'Park Circus', 'Camac Street', 'Elgin Road', 'Loudon Street', 'Rawdon Street',
        'Ballygunge', 'Golpark', 'Lake Gardens', 'Jodhpur Park', 'Hazra',
        'Kalighat', 'Rashbehari Avenue', 'Gariahat', 'Ballygunge Place', 'Southern Avenue',
        'Kasba', 'Garfa', 'Jadavpur', 'Santoshpur', 'Baghajatin',
        'Naktala', 'Golf Green', 'Regent Park', 'Tollygunge', 'New Alipore',
        'Tiljala', 'Topsia', 'Tangra', 'Phoolbagan', 'Sealdah',
        'Burrabazar', 'Bowbazar', 'Chandni Chowk', 'Shyambazar', 'Girish Park',
        'Shobhabazar', 'Hatibagan', 'Maniktala', 'Ultadanga', 'Kankurgachi',
        'Phoolbagan', 'Sealdah', 'Park Circus', 'Taltala', 'New Market',
        'Esplanade', 'BBD Bagh', 'Dalhousie', 'Burrabazar', 'Bowbazar'
    ],
    'Howrah': [
        'Howrah City', 'Shibpur', 'Bally', 'Uttarpara', 'Rishra',
        'Serampore', 'Chandannagar', 'Bhadreswar', 'Bauria', 'Domjur',
        'Jagatballavpur', 'Panchla', 'Sankrail', 'Uluberia', 'Amta',
        'Station Road', 'MG Road', 'Grand Trunk Road', 'Kolkata Road', 'Dankuni Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Durgapur': [
        'Durgapur City', 'Asansol', 'Raniganj', 'Kulti', 'Burnpur',
        'Jamuria', 'Pandabeswar', 'Faridpur', 'Durgapur', 'Asansol',
        'City Centre', 'Benachity', 'Bidhan Nagar', 'Durgapur Steel Plant', 'Durgapur Barrage',
        'Station Road', 'MG Road', 'Ring Road', 'Asansol Road', 'Kolkata Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Asansol': [
        'Asansol City', 'Durgapur', 'Raniganj', 'Kulti', 'Burnpur',
        'Jamuria', 'Pandabeswar', 'Faridpur', 'Durgapur', 'Raniganj',
        'Station Road', 'MG Road', 'Ring Road', 'Durgapur Road', 'Kolkata Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Siliguri': [
        'Siliguri City', 'Darjeeling', 'Kurseong', 'Kalimpong', 'Jalpaiguri',
        'Malbazar', 'Dhupguri', 'Alipurduar', 'Cooch Behar', 'Dinhata',
        'Sevoke Road', 'Hill Cart Road', 'Tenzing Norgay Road', 'Darjeeling Road', 'Jalpaiguri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bardhaman': [
        'Bardhaman City', 'Durgapur', 'Asansol', 'Katwa', 'Kalna',
        'Memari', 'Guskara', 'Bhatar', 'Purbasthali', 'Manteswar',
        'Station Road', 'MG Road', 'Ring Road', 'Durgapur Road', 'Katwa Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Burdwan': [
        'Bardhaman City', 'Durgapur', 'Asansol', 'Katwa', 'Kalna',
        'Memari', 'Guskara', 'Bhatar', 'Purbasthali', 'Manteswar',
        'Station Road', 'MG Road', 'Ring Road', 'Durgapur Road', 'Katwa Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Malda': [
        'Malda City', 'English Bazar', 'Old Malda', 'Chanchal', 'Harishchandrapur',
        'Ratua', 'Bamongola', 'Habibpur', 'Kaliachak', 'Manikchak',
        'Station Road', 'MG Road', 'Ring Road', 'English Bazar Road', 'Murshidabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kharagpur': [
        'Kharagpur City', 'Midnapore', 'Jhargram', 'Ghatal', 'Kharagpur',
        'Narayangarh', 'Sabang', 'Pingla', 'Debra', 'Daspur',
        'IIT Kharagpur', 'Station Road', 'MG Road', 'Ring Road', 'Midnapore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Krishnanagar': [
        'Krishnanagar City', 'Nadia', 'Ranaghat', 'Shantipur', 'Kalyani',
        'Chakdaha', 'Haringhata', 'Krishnanagar', 'Ranaghat', 'Shantipur',
        'Station Road', 'MG Road', 'Ring Road', 'Kalyani Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nadia': [
        'Krishnanagar City', 'Nadia', 'Ranaghat', 'Shantipur', 'Kalyani',
        'Chakdaha', 'Haringhata', 'Krishnanagar', 'Ranaghat', 'Shantipur',
        'Station Road', 'MG Road', 'Ring Road', 'Kalyani Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ranaghat': [
        'Ranaghat City', 'Krishnanagar', 'Shantipur', 'Kalyani', 'Chakdaha',
        'Haringhata', 'Nadia', 'Krishnanagar', 'Shantipur', 'Kalyani',
        'Station Road', 'MG Road', 'Ring Road', 'Krishnanagar Road', 'Kalyani Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kalyani': [
        'Kalyani City', 'Krishnanagar', 'Ranaghat', 'Shantipur', 'Chakdaha',
        'Haringhata', 'Nadia', 'Krishnanagar', 'Ranaghat', 'Shantipur',
        'Station Road', 'MG Road', 'Ring Road', 'Krishnanagar Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Midnapore': [
        'Midnapore City', 'Kharagpur', 'Jhargram', 'Ghatal', 'Narayangarh',
        'Sabang', 'Pingla', 'Debra', 'Daspur', 'Kharagpur',
        'Station Road', 'MG Road', 'Ring Road', 'Kharagpur Road', 'Jhargram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Medinipur': [
        'Midnapore City', 'Kharagpur', 'Jhargram', 'Ghatal', 'Narayangarh',
        'Sabang', 'Pingla', 'Debra', 'Daspur', 'Kharagpur',
        'Station Road', 'MG Road', 'Ring Road', 'Kharagpur Road', 'Jhargram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jhargram': [
        'Jhargram City', 'Midnapore', 'Kharagpur', 'Ghatal', 'Narayangarh',
        'Sabang', 'Pingla', 'Debra', 'Daspur', 'Kharagpur',
        'Station Road', 'MG Road', 'Ring Road', 'Midnapore Road', 'Kharagpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Barasat': [
        'Barasat City', 'Kolkata', 'Dum Dum', 'Rajarhat', 'New Town',
        'Salt Lake', 'Bidhannagar', 'Kolkata', 'Dum Dum', 'Rajarhat',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Dum Dum Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dum Dum': [
        'Dum Dum City', 'Kolkata', 'Barasat', 'Rajarhat', 'New Town',
        'Salt Lake', 'Bidhannagar', 'Kolkata', 'Barasat', 'Rajarhat',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Barasat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rajarhat': [
        'Rajarhat City', 'Kolkata', 'New Town', 'Salt Lake', 'Bidhannagar',
        'Dum Dum', 'Barasat', 'Kolkata', 'New Town', 'Salt Lake',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'New Town Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'New Town': [
        'New Town City', 'Kolkata', 'Rajarhat', 'Salt Lake', 'Bidhannagar',
        'Dum Dum', 'Barasat', 'Kolkata', 'Rajarhat', 'Salt Lake',
        'Action Area I', 'Action Area II', 'Action Area III', 'Sector V', 'Sector I',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Rajarhat Road'
    ],
    'Bidhannagar': [
        'Salt Lake City', 'Kolkata', 'New Town', 'Rajarhat', 'Dum Dum',
        'Barasat', 'Kolkata', 'New Town', 'Rajarhat', 'Dum Dum',
        'Sector I', 'Sector II', 'Sector III', 'Sector IV', 'Sector V',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'New Town Road'
    ],
    'Salt Lake': [
        'Salt Lake City', 'Kolkata', 'New Town', 'Rajarhat', 'Bidhannagar',
        'Dum Dum', 'Barasat', 'Kolkata', 'New Town', 'Rajarhat',
        'Sector I', 'Sector II', 'Sector III', 'Sector IV', 'Sector V',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'New Town Road'
    ],
    'Serampore': [
        'Serampore City', 'Howrah', 'Chandannagar', 'Rishra', 'Uttarpara',
        'Bally', 'Shibpur', 'Howrah', 'Chandannagar', 'Rishra',
        'Station Road', 'MG Road', 'Ring Road', 'Howrah Road', 'Chandannagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chandannagar': [
        'Chandannagar City', 'Howrah', 'Serampore', 'Rishra', 'Uttarpara',
        'Bally', 'Shibpur', 'Howrah', 'Serampore', 'Rishra',
        'Station Road', 'MG Road', 'Ring Road', 'Howrah Road', 'Serampore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rishra': [
        'Rishra City', 'Howrah', 'Serampore', 'Chandannagar', 'Uttarpara',
        'Bally', 'Shibpur', 'Howrah', 'Serampore', 'Chandannagar',
        'Station Road', 'MG Road', 'Ring Road', 'Howrah Road', 'Serampore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Uttarpara': [
        'Uttarpara City', 'Howrah', 'Serampore', 'Chandannagar', 'Rishra',
        'Bally', 'Shibpur', 'Howrah', 'Serampore', 'Chandannagar',
        'Station Road', 'MG Road', 'Ring Road', 'Howrah Road', 'Serampore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bally': [
        'Bally City', 'Howrah', 'Uttarpara', 'Rishra', 'Serampore',
        'Chandannagar', 'Shibpur', 'Howrah', 'Uttarpara', 'Rishra',
        'Station Road', 'MG Road', 'Ring Road', 'Howrah Road', 'Uttarpara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jalpaiguri': [
        'Jalpaiguri City', 'Siliguri', 'Alipurduar', 'Malbazar', 'Dhupguri',
        'Maynaguri', 'Nagrakata', 'Jalpaiguri', 'Siliguri', 'Alipurduar',
        'Station Road', 'MG Road', 'Ring Road', 'Siliguri Road', 'Alipurduar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Alipurduar': [
        'Alipurduar City', 'Jalpaiguri', 'Siliguri', 'Malbazar', 'Dhupguri',
        'Maynaguri', 'Nagrakata', 'Jalpaiguri', 'Siliguri', 'Malbazar',
        'Station Road', 'MG Road', 'Ring Road', 'Jalpaiguri Road', 'Siliguri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Cooch Behar': [
        'Cooch Behar City', 'Alipurduar', 'Dinhata', 'Mathabhanga', 'Tufanganj',
        'Sitalkuchi', 'Dinhata', 'Mathabhanga', 'Tufanganj', 'Sitalkuchi',
        'Station Road', 'MG Road', 'Ring Road', 'Alipurduar Road', 'Dinhata Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Darjeeling': [
        'Darjeeling City', 'Kurseong', 'Kalimpong', 'Mirik', 'Sukna',
        'Siliguri', 'Kurseong', 'Kalimpong', 'Mirik', 'Sukna',
        'Mall Road', 'Chowrasta', 'Station Road', 'MG Road', 'Siliguri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kurseong': [
        'Kurseong City', 'Darjeeling', 'Kalimpong', 'Mirik', 'Sukna',
        'Siliguri', 'Darjeeling', 'Kalimpong', 'Mirik', 'Sukna',
        'Station Road', 'MG Road', 'Ring Road', 'Darjeeling Road', 'Siliguri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kalimpong': [
        'Kalimpong City', 'Darjeeling', 'Kurseong', 'Mirik', 'Sukna',
        'Siliguri', 'Darjeeling', 'Kurseong', 'Mirik', 'Sukna',
        'Station Road', 'MG Road', 'Ring Road', 'Darjeeling Road', 'Siliguri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Murshidabad': [
        'Berhampore City', 'Murshidabad', 'Baharampur', 'Kandi', 'Jangipur',
        'Lalbagh', 'Nawabganj', 'Domkal', 'Suti', 'Sagardighi',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Malda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Berhampore': [
        'Berhampore City', 'Murshidabad', 'Baharampur', 'Kandi', 'Jangipur',
        'Lalbagh', 'Nawabganj', 'Domkal', 'Suti', 'Sagardighi',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Malda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Baharampur': [
        'Berhampore City', 'Murshidabad', 'Baharampur', 'Kandi', 'Jangipur',
        'Lalbagh', 'Nawabganj', 'Domkal', 'Suti', 'Sagardighi',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Malda Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Purulia': [
        'Purulia City', 'Jhalda', 'Raghunathpur', 'Adra', 'Barakar',
        'Chas', 'Balarampur', 'Arsha', 'Baghmundi', 'Hura',
        'Station Road', 'MG Road', 'Ring Road', 'Jhalda Road', 'Raghunathpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bankura': [
        'Bankura City', 'Bishnupur', 'Sonamukhi', 'Khatra', 'Raipur',
        'Indpur', 'Chhatna', 'Gangajalghati', 'Mejhia', 'Saltora',
        'Station Road', 'MG Road', 'Ring Road', 'Bishnupur Road', 'Khatra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bishnupur': [
        'Bishnupur City', 'Bankura', 'Sonamukhi', 'Khatra', 'Raipur',
        'Indpur', 'Chhatna', 'Gangajalghati', 'Mejhia', 'Saltora',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Bankura Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hooghly': [
        'Chinsurah City', 'Hooghly', 'Chandannagar', 'Serampore', 'Rishra',
        'Uttarpara', 'Bally', 'Shibpur', 'Howrah', 'Chandannagar',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Chandannagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chinsurah': [
        'Chinsurah City', 'Hooghly', 'Chandannagar', 'Serampore', 'Rishra',
        'Uttarpara', 'Bally', 'Shibpur', 'Howrah', 'Chandannagar',
        'Station Road', 'MG Road', 'Ring Road', 'Kolkata Road', 'Chandannagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Birbhum': [
        'Suri City', 'Rampurhat', 'Bolpur', 'Sainthia', 'Dubrajpur',
        'Nanoor', 'Illambazar', 'Suri', 'Rampurhat', 'Bolpur',
        'Station Road', 'MG Road', 'Ring Road', 'Rampurhat Road', 'Bolpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Suri': [
        'Suri City', 'Rampurhat', 'Bolpur', 'Sainthia', 'Dubrajpur',
        'Nanoor', 'Illambazar', 'Suri', 'Rampurhat', 'Bolpur',
        'Station Road', 'MG Road', 'Ring Road', 'Rampurhat Road', 'Bolpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bolpur': [
        'Bolpur City', 'Shantiniketan', 'Suri', 'Rampurhat', 'Sainthia',
        'Dubrajpur', 'Nanoor', 'Illambazar', 'Shantiniketan', 'Suri',
        'Shantiniketan', 'Station Road', 'MG Road', 'Ring Road', 'Suri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Shantiniketan': [
        'Bolpur City', 'Shantiniketan', 'Suri', 'Rampurhat', 'Sainthia',
        'Dubrajpur', 'Nanoor', 'Illambazar', 'Shantiniketan', 'Suri',
        'Visva Bharati', 'Station Road', 'MG Road', 'Ring Road', 'Suri Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rampurhat': [
        'Rampurhat City', 'Suri', 'Bolpur', 'Sainthia', 'Dubrajpur',
        'Nanoor', 'Illambazar', 'Suri', 'Bolpur', 'Sainthia',
        'Station Road', 'MG Road', 'Ring Road', 'Suri Road', 'Bolpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Katwa': [
        'Katwa City', 'Bardhaman', 'Kalna', 'Memari', 'Guskara',
        'Bhatar', 'Purbasthali', 'Manteswar', 'Bardhaman', 'Kalna',
        'Station Road', 'MG Road', 'Ring Road', 'Bardhaman Road', 'Kalna Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kalna': [
        'Kalna City', 'Bardhaman', 'Katwa', 'Memari', 'Guskara',
        'Bhatar', 'Purbasthali', 'Manteswar', 'Bardhaman', 'Katwa',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Bardhaman Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Raniganj': [
        'Raniganj City', 'Asansol', 'Durgapur', 'Kulti', 'Burnpur',
        'Jamuria', 'Pandabeswar', 'Faridpur', 'Asansol', 'Durgapur',
        'Station Road', 'MG Road', 'Ring Road', 'Asansol Road', 'Durgapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kulti': [
        'Kulti City', 'Asansol', 'Durgapur', 'Raniganj', 'Burnpur',
        'Jamuria', 'Pandabeswar', 'Faridpur', 'Asansol', 'Durgapur',
        'Station Road', 'MG Road', 'Ring Road', 'Asansol Road', 'Durgapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Burnpur': [
        'Burnpur City', 'Asansol', 'Durgapur', 'Raniganj', 'Kulti',
        'Jamuria', 'Pandabeswar', 'Faridpur', 'Asansol', 'Durgapur',
        'Station Road', 'MG Road', 'Ring Road', 'Asansol Road', 'Durgapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jalangi': [
        'Jalangi City', 'Krishnanagar', 'Ranaghat', 'Shantipur', 'Kalyani',
        'Chakdaha', 'Haringhata', 'Krishnanagar', 'Ranaghat', 'Shantipur',
        'Station Road', 'MG Road', 'Ring Road', 'Krishnanagar Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Shantipur': [
        'Shantipur City', 'Krishnanagar', 'Ranaghat', 'Kalyani', 'Chakdaha',
        'Haringhata', 'Nadia', 'Krishnanagar', 'Ranaghat', 'Kalyani',
        'Station Road', 'MG Road', 'Ring Road', 'Krishnanagar Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chakdaha': [
        'Chakdaha City', 'Krishnanagar', 'Ranaghat', 'Shantipur', 'Kalyani',
        'Haringhata', 'Nadia', 'Krishnanagar', 'Ranaghat', 'Shantipur',
        'Station Road', 'MG Road', 'Ring Road', 'Krishnanagar Road', 'Ranaghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ghatal': [
        'Ghatal City', 'Midnapore', 'Kharagpur', 'Jhargram', 'Narayangarh',
        'Sabang', 'Pingla', 'Debra', 'Daspur', 'Kharagpur',
        'Station Road', 'MG Road', 'Ring Road', 'Midnapore Road', 'Kharagpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Narayangarh': [
        'Narayangarh City', 'Midnapore', 'Kharagpur', 'Jhargram', 'Ghatal',
        'Sabang', 'Pingla', 'Debra', 'Daspur', 'Kharagpur',
        'Station Road', 'MG Road', 'Ring Road', 'Midnapore Road', 'Kharagpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Contai': [
        'Contai City', 'Tamluk', 'Haldia', 'Digha', 'Mandarmani',
        'Kanthi', 'Tamluk', 'Haldia', 'Digha', 'Mandarmani',
        'Station Road', 'MG Road', 'Ring Road', 'Tamluk Road', 'Haldia Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tamluk': [
        'Tamluk City', 'Contai', 'Haldia', 'Digha', 'Mandarmani',
        'Kanthi', 'Contai', 'Haldia', 'Digha', 'Mandarmani',
        'Station Road', 'MG Road', 'Ring Road', 'Contai Road', 'Haldia Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Haldia': [
        'Haldia City', 'Tamluk', 'Contai', 'Digha', 'Mandarmani',
        'Kanthi', 'Tamluk', 'Contai', 'Digha', 'Mandarmani',
        'Port Area', 'Station Road', 'MG Road', 'Ring Road', 'Tamluk Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Digha': [
        'Digha City', 'Tamluk', 'Contai', 'Haldia', 'Mandarmani',
        'Kanthi', 'Tamluk', 'Contai', 'Haldia', 'Mandarmani',
        'Beach Area', 'Station Road', 'MG Road', 'Ring Road', 'Tamluk Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mandarmani': [
        'Mandarmani City', 'Digha', 'Tamluk', 'Contai', 'Haldia',
        'Kanthi', 'Digha', 'Tamluk', 'Contai', 'Haldia',
        'Beach Area', 'Station Road', 'MG Road', 'Ring Road', 'Digha Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kanthi': [
        'Contai City', 'Tamluk', 'Haldia', 'Digha', 'Mandarmani',
        'Kanthi', 'Tamluk', 'Haldia', 'Digha', 'Mandarmani',
        'Station Road', 'MG Road', 'Ring Road', 'Tamluk Road', 'Haldia Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Balurghat': [
        'Balurghat City', 'Malda', 'Raiganj', 'Gangarampur', 'Kumarganj',
        'Tapan', 'Harirampur', 'Balurghat', 'Malda', 'Raiganj',
        'Station Road', 'MG Road', 'Ring Road', 'Malda Road', 'Raiganj Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Raiganj': [
        'Raiganj City', 'Balurghat', 'Malda', 'Gangarampur', 'Kumarganj',
        'Tapan', 'Harirampur', 'Balurghat', 'Malda', 'Gangarampur',
        'Station Road', 'MG Road', 'Ring Road', 'Malda Road', 'Balurghat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gangarampur': [
        'Gangarampur City', 'Balurghat', 'Raiganj', 'Malda', 'Kumarganj',
        'Tapan', 'Harirampur', 'Balurghat', 'Raiganj', 'Malda',
        'Station Road', 'MG Road', 'Ring Road', 'Balurghat Road', 'Raiganj Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'English Bazar': [
        'Malda City', 'English Bazar', 'Old Malda', 'Chanchal', 'Harishchandrapur',
        'Ratua', 'Bamongola', 'Habibpur', 'Kaliachak', 'Manikchak',
        'Station Road', 'MG Road', 'Ring Road', 'English Bazar Road', 'Murshidabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
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
        'Pal Road', 'Mandore', 'Bilara', 'Phalodi', 'Osian',
        'Jodhpur City', 'Ratanada', 'Shastri Nagar', 'Shastri Circle', 'Umaid Bhawan',
        'Pal Road', 'Mandore', 'Bilara', 'Phalodi', 'Osian',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Pali Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kota': [
        'Kota City', 'Baran', 'Bundi', 'Jhalawar', 'Ramganj Mandi',
        'Sangod', 'Kota', 'Baran', 'Bundi', 'Jhalawar',
        'Station Road', 'MG Road', 'Ring Road', 'Bundi Road', 'Jhalawar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bikaner': [
        'Bikaner City', 'Nokha', 'Lunkaransar', 'Kolayat', 'Pugal',
        'Dungargarh', 'Raisinghnagar', 'Anupgarh', 'Bikaner', 'Nokha',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Jaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ajmer': [
        'Ajmer City', 'Pushkar', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Kekri', 'Sarwar', 'Ajmer', 'Pushkar', 'Kishangarh',
        'Station Road', 'MG Road', 'Ring Road', 'Jaipur Road', 'Pushkar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Udaipur': [
        'Udaipur City', 'Rajsamand', 'Nathdwara', 'Salumbar', 'Gogunda',
        'Kumbhalgarh', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Station Road', 'MG Road', 'Ring Road', 'Rajsamand Road', 'Nathdwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhilwara': [
        'Bhilwara City', 'Asind', 'Mandal', 'Shahpura', 'Raipur',
        'Gulabpura', 'Mandalgarh', 'Bhilwara', 'Asind', 'Mandal',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Chittorgarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Alwar': [
        'Alwar City', 'Bhiwadi', 'Behror', 'Tijara', 'Kishangarh',
        'Rajgarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Delhi Road', 'Jaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bharatpur': [
        'Bharatpur City', 'Deeg', 'Bayana', 'Kaman', 'Nadbai',
        'Kumher', 'Weir', 'Bharatpur', 'Deeg', 'Bayana',
        'Station Road', 'MG Road', 'Ring Road', 'Agra Road', 'Mathura Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sikar': [
        'Sikar City', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh', 'Neem Ka Thana',
        'Sri Madhopur', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Jaipur Road', 'Fatehpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pali': [
        'Pali City', 'Jodhpur', 'Sojat', 'Jaitaran', 'Raipur',
        'Falna', 'Marwar Junction', 'Pali', 'Sojat', 'Jaitaran',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Sojat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chittorgarh': [
        'Chittorgarh City', 'Bhilwara', 'Pratapgarh', 'Banswara', 'Dungarpur',
        'Begun', 'Nimbahera', 'Chittorgarh', 'Bhilwara', 'Pratapgarh',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chittor': [
        'Chittorgarh City', 'Bhilwara', 'Pratapgarh', 'Banswara', 'Dungarpur',
        'Begun', 'Nimbahera', 'Chittorgarh', 'Bhilwara', 'Pratapgarh',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Banswara': [
        'Banswara City', 'Dungarpur', 'Pratapgarh', 'Chittorgarh', 'Bhilwara',
        'Ghatol', 'Kushalgarh', 'Banswara', 'Dungarpur', 'Pratapgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Dungarpur Road', 'Pratapgarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dungarpur': [
        'Dungarpur City', 'Banswara', 'Pratapgarh', 'Chittorgarh', 'Bhilwara',
        'Ghatol', 'Kushalgarh', 'Banswara', 'Pratapgarh', 'Chittorgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Banswara Road', 'Pratapgarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pratapgarh': [
        'Pratapgarh City', 'Chittorgarh', 'Banswara', 'Dungarpur', 'Bhilwara',
        'Begun', 'Nimbahera', 'Chittorgarh', 'Banswara', 'Dungarpur',
        'Station Road', 'MG Road', 'Ring Road', 'Chittorgarh Road', 'Banswara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jhalawar': [
        'Jhalawar City', 'Kota', 'Baran', 'Bundi', 'Ramganj Mandi',
        'Sangod', 'Kota', 'Baran', 'Bundi', 'Ramganj Mandi',
        'Station Road', 'MG Road', 'Ring Road', 'Kota Road', 'Baran Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Baran': [
        'Baran City', 'Kota', 'Jhalawar', 'Bundi', 'Ramganj Mandi',
        'Sangod', 'Kota', 'Jhalawar', 'Bundi', 'Ramganj Mandi',
        'Station Road', 'MG Road', 'Ring Road', 'Kota Road', 'Jhalawar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bundi': [
        'Bundi City', 'Kota', 'Jhalawar', 'Baran', 'Ramganj Mandi',
        'Sangod', 'Kota', 'Jhalawar', 'Baran', 'Ramganj Mandi',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Kota Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tonk': [
        'Tonk City', 'Jaipur', 'Deoli', 'Uniara', 'Malpura',
        'Niwai', 'Tonk', 'Deoli', 'Uniara', 'Malpura',
        'Station Road', 'MG Road', 'Ring Road', 'Jaipur Road', 'Deoli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dausa': [
        'Dausa City', 'Jaipur', 'Sikar', 'Lalsot', 'Baswa',
        'Mahuwa', 'Dausa', 'Lalsot', 'Baswa', 'Mahuwa',
        'Station Road', 'MG Road', 'Ring Road', 'Jaipur Road', 'Sikar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Karauli': [
        'Karauli City', 'Sawai Madhopur', 'Dausa', 'Hindaun', 'Todabhim',
        'Sapotra', 'Karauli', 'Sawai Madhopur', 'Dausa', 'Hindaun',
        'Station Road', 'MG Road', 'Ring Road', 'Sawai Madhopur Road', 'Dausa Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sawai Madhopur': [
        'Sawai Madhopur City', 'Karauli', 'Dausa', 'Hindaun', 'Todabhim',
        'Sapotra', 'Karauli', 'Dausa', 'Hindaun', 'Todabhim',
        'Ranthambore', 'Station Road', 'MG Road', 'Ring Road', 'Karauli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dholpur': [
        'Dholpur City', 'Bharatpur', 'Agra', 'Mathura', 'Morena',
        'Rajasthan', 'Bharatpur', 'Agra', 'Mathura', 'Morena',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Agra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nagaur': [
        'Nagaur City', 'Jodhpur', 'Ajmer', 'Makrana', 'Didwana',
        'Merta', 'Parbatsar', 'Nagaur', 'Makrana', 'Didwana',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Ajmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jalore': [
        'Jalore City', 'Jodhpur', 'Pali', 'Sirohi', 'Sanchore',
        'Bhinmal', 'Ahore', 'Jalore', 'Pali', 'Sirohi',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Pali Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sirohi': [
        'Sirohi City', 'Jalore', 'Pali', 'Jodhpur', 'Sanchore',
        'Bhinmal', 'Ahore', 'Jalore', 'Pali', 'Jodhpur',
        'Station Road', 'MG Road', 'Ring Road', 'Jalore Road', 'Pali Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Barmer': [
        'Barmer City', 'Jaisalmer', 'Jodhpur', 'Balotra', 'Siwana',
        'Pachpadra', 'Gudamalani', 'Barmer', 'Jaisalmer', 'Jodhpur',
        'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road', 'Jodhpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jaisalmer': [
        'Jaisalmer City', 'Barmer', 'Pokaran', 'Sam', 'Khuri',
        'Lodhruva', 'Amar Sagar', 'Jaisalmer', 'Barmer', 'Pokaran',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Barmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hanumangarh': [
        'Hanumangarh City', 'Ganganagar', 'Bhadra', 'Nohar', 'Sangaria',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Ganganagar', 'Bhadra',
        'Station Road', 'MG Road', 'Ring Road', 'Ganganagar Road', 'Bhadra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ganganagar': [
        'Ganganagar City', 'Hanumangarh', 'Bhadra', 'Nohar', 'Sangaria',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Bhadra', 'Nohar',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Bhadra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sri Ganganagar': [
        'Ganganagar City', 'Hanumangarh', 'Bhadra', 'Nohar', 'Sangaria',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Bhadra', 'Nohar',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Bhadra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Churu': [
        'Churu City', 'Sujangarh', 'Ratangarh', 'Sardarshahar', 'Taranagar',
        'Rajgarh', 'Churu', 'Sujangarh', 'Ratangarh', 'Sardarshahar',
        'Station Road', 'MG Road', 'Ring Road', 'Bikaner Road', 'Sujangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jhunjhunu': [
        'Jhunjhunu City', 'Sikar', 'Churu', 'Nawalgarh', 'Khetri',
        'Udaipurwati', 'Chirawa', 'Jhunjhunu', 'Sikar', 'Churu',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Churu Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rajsamand': [
        'Rajsamand City', 'Udaipur', 'Nathdwara', 'Salumbar', 'Gogunda',
        'Kumbhalgarh', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Nathdwara',
        'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road', 'Nathdwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Beawar': [
        'Beawar City', 'Ajmer', 'Kishangarh', 'Nasirabad', 'Kekri',
        'Sarwar', 'Ajmer', 'Kishangarh', 'Nasirabad', 'Kekri',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Kishangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kishangarh': [
        'Kishangarh City', 'Ajmer', 'Beawar', 'Nasirabad', 'Kekri',
        'Sarwar', 'Ajmer', 'Beawar', 'Nasirabad', 'Kekri',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Beawar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pushkar': [
        'Pushkar City', 'Ajmer', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Kekri', 'Sarwar', 'Ajmer', 'Kishangarh', 'Beawar',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nathdwara': [
        'Nathdwara City', 'Udaipur', 'Rajsamand', 'Salumbar', 'Gogunda',
        'Kumbhalgarh', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mount Abu': [
        'Mount Abu City', 'Sirohi', 'Abu Road', 'Pindwara', 'Reodar',
        'Sheoganj', 'Sirohi', 'Abu Road', 'Pindwara', 'Reodar',
        'Station Road', 'MG Road', 'Ring Road', 'Sirohi Road', 'Abu Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Abu Road': [
        'Abu Road City', 'Mount Abu', 'Sirohi', 'Pindwara', 'Reodar',
        'Sheoganj', 'Mount Abu', 'Sirohi', 'Pindwara', 'Reodar',
        'Station Road', 'MG Road', 'Ring Road', 'Mount Abu Road', 'Sirohi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhiwadi': [
        'Bhiwadi City', 'Alwar', 'Behror', 'Tijara', 'Kishangarh',
        'Rajgarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Behror',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Delhi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Behror': [
        'Behror City', 'Alwar', 'Bhiwadi', 'Tijara', 'Kishangarh',
        'Rajgarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Bhiwadi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rajgarh': [
        'Rajgarh City', 'Alwar', 'Bhiwadi', 'Behror', 'Tijara',
        'Kishangarh', 'Laxmangarh', 'Thanagazi', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Bhiwadi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Laxmangarh': [
        'Laxmangarh City', 'Alwar', 'Bhiwadi', 'Behror', 'Tijara',
        'Kishangarh', 'Rajgarh', 'Thanagazi', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Bhiwadi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Makrana': [
        'Makrana City', 'Nagaur', 'Jodhpur', 'Ajmer', 'Didwana',
        'Merta', 'Parbatsar', 'Nagaur', 'Jodhpur', 'Ajmer',
        'Station Road', 'MG Road', 'Ring Road', 'Nagaur Road', 'Jodhpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Didwana': [
        'Didwana City', 'Nagaur', 'Makrana', 'Jodhpur', 'Ajmer',
        'Merta', 'Parbatsar', 'Nagaur', 'Makrana', 'Jodhpur',
        'Station Road', 'MG Road', 'Ring Road', 'Nagaur Road', 'Makrana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Merta': [
        'Merta City', 'Nagaur', 'Makrana', 'Didwana', 'Jodhpur',
        'Ajmer', 'Parbatsar', 'Nagaur', 'Makrana', 'Didwana',
        'Station Road', 'MG Road', 'Ring Road', 'Nagaur Road', 'Makrana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Phalodi': [
        'Phalodi City', 'Jodhpur', 'Bikaner', 'Pokaran', 'Jaisalmer',
        'Barmer', 'Pokaran', 'Jodhpur', 'Bikaner', 'Jaisalmer',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Bikaner Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pokaran': [
        'Pokaran City', 'Jaisalmer', 'Barmer', 'Jodhpur', 'Phalodi',
        'Bikaner', 'Jaisalmer', 'Barmer', 'Jodhpur', 'Phalodi',
        'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road', 'Barmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Osian': [
        'Osian City', 'Jodhpur', 'Phalodi', 'Bilara', 'Bhopalgarh',
        'Shergarh', 'Jodhpur', 'Phalodi', 'Bilara', 'Bhopalgarh',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bilara': [
        'Bilara City', 'Jodhpur', 'Osian', 'Phalodi', 'Bhopalgarh',
        'Shergarh', 'Jodhpur', 'Osian', 'Phalodi', 'Bhopalgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Osian Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sojat': [
        'Sojat City', 'Pali', 'Jodhpur', 'Jaitaran', 'Raipur',
        'Falna', 'Marwar Junction', 'Pali', 'Jodhpur', 'Jaitaran',
        'Station Road', 'MG Road', 'Ring Road', 'Pali Road', 'Jodhpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jaitaran': [
        'Jaitaran City', 'Pali', 'Sojat', 'Jodhpur', 'Raipur',
        'Falna', 'Marwar Junction', 'Pali', 'Sojat', 'Jodhpur',
        'Station Road', 'MG Road', 'Ring Road', 'Pali Road', 'Sojat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Balotra': [
        'Balotra City', 'Barmer', 'Jaisalmer', 'Jodhpur', 'Siwana',
        'Pachpadra', 'Gudamalani', 'Barmer', 'Jaisalmer', 'Jodhpur',
        'Station Road', 'MG Road', 'Ring Road', 'Barmer Road', 'Jaisalmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Siwana': [
        'Siwana City', 'Barmer', 'Balotra', 'Jaisalmer', 'Jodhpur',
        'Pachpadra', 'Gudamalani', 'Barmer', 'Balotra', 'Jaisalmer',
        'Station Road', 'MG Road', 'Ring Road', 'Barmer Road', 'Balotra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nohar': [
        'Nohar City', 'Hanumangarh', 'Ganganagar', 'Bhadra', 'Sangaria',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Ganganagar', 'Bhadra',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Ganganagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhadra': [
        'Bhadra City', 'Hanumangarh', 'Ganganagar', 'Nohar', 'Sangaria',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Ganganagar', 'Nohar',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Ganganagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sangaria': [
        'Sangaria City', 'Hanumangarh', 'Ganganagar', 'Bhadra', 'Nohar',
        'Pilibanga', 'Rawatsar', 'Hanumangarh', 'Ganganagar', 'Bhadra',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Ganganagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pilibanga': [
        'Pilibanga City', 'Hanumangarh', 'Ganganagar', 'Bhadra', 'Nohar',
        'Sangaria', 'Rawatsar', 'Hanumangarh', 'Ganganagar', 'Bhadra',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Ganganagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rawatsar': [
        'Rawatsar City', 'Hanumangarh', 'Ganganagar', 'Bhadra', 'Nohar',
        'Sangaria', 'Pilibanga', 'Hanumangarh', 'Ganganagar', 'Bhadra',
        'Station Road', 'MG Road', 'Ring Road', 'Hanumangarh Road', 'Ganganagar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sujangarh': [
        'Sujangarh City', 'Churu', 'Ratangarh', 'Sardarshahar', 'Taranagar',
        'Rajgarh', 'Churu', 'Ratangarh', 'Sardarshahar', 'Taranagar',
        'Station Road', 'MG Road', 'Ring Road', 'Churu Road', 'Ratangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ratangarh': [
        'Ratangarh City', 'Churu', 'Sujangarh', 'Sardarshahar', 'Taranagar',
        'Rajgarh', 'Churu', 'Sujangarh', 'Sardarshahar', 'Taranagar',
        'Station Road', 'MG Road', 'Ring Road', 'Churu Road', 'Sujangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sardarshahar': [
        'Sardarshahar City', 'Churu', 'Sujangarh', 'Ratangarh', 'Taranagar',
        'Rajgarh', 'Churu', 'Sujangarh', 'Ratangarh', 'Taranagar',
        'Station Road', 'MG Road', 'Ring Road', 'Churu Road', 'Sujangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Taranagar': [
        'Taranagar City', 'Churu', 'Sujangarh', 'Ratangarh', 'Sardarshahar',
        'Rajgarh', 'Churu', 'Sujangarh', 'Ratangarh', 'Sardarshahar',
        'Station Road', 'MG Road', 'Ring Road', 'Churu Road', 'Sujangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nawalgarh': [
        'Nawalgarh City', 'Jhunjhunu', 'Sikar', 'Churu', 'Khetri',
        'Udaipurwati', 'Chirawa', 'Jhunjhunu', 'Sikar', 'Churu',
        'Station Road', 'MG Road', 'Ring Road', 'Jhunjhunu Road', 'Sikar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Khetri': [
        'Khetri City', 'Jhunjhunu', 'Sikar', 'Churu', 'Nawalgarh',
        'Udaipurwati', 'Chirawa', 'Jhunjhunu', 'Sikar', 'Churu',
        'Station Road', 'MG Road', 'Ring Road', 'Jhunjhunu Road', 'Sikar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Udaipurwati': [
        'Udaipurwati City', 'Jhunjhunu', 'Sikar', 'Churu', 'Nawalgarh',
        'Khetri', 'Chirawa', 'Jhunjhunu', 'Sikar', 'Churu',
        'Station Road', 'MG Road', 'Ring Road', 'Jhunjhunu Road', 'Sikar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chirawa': [
        'Chirawa City', 'Jhunjhunu', 'Sikar', 'Churu', 'Nawalgarh',
        'Khetri', 'Udaipurwati', 'Jhunjhunu', 'Sikar', 'Churu',
        'Station Road', 'MG Road', 'Ring Road', 'Jhunjhunu Road', 'Sikar Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Lalsot': [
        'Lalsot City', 'Dausa', 'Jaipur', 'Sikar', 'Baswa',
        'Mahuwa', 'Dausa', 'Jaipur', 'Sikar', 'Baswa',
        'Station Road', 'MG Road', 'Ring Road', 'Dausa Road', 'Jaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Baswa': [
        'Baswa City', 'Dausa', 'Lalsot', 'Jaipur', 'Sikar',
        'Mahuwa', 'Dausa', 'Lalsot', 'Jaipur', 'Sikar',
        'Station Road', 'MG Road', 'Ring Road', 'Dausa Road', 'Lalsot Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mahuwa': [
        'Mahuwa City', 'Dausa', 'Lalsot', 'Baswa', 'Jaipur',
        'Sikar', 'Dausa', 'Lalsot', 'Baswa', 'Jaipur',
        'Station Road', 'MG Road', 'Ring Road', 'Dausa Road', 'Lalsot Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hindaun': [
        'Hindaun City', 'Karauli', 'Sawai Madhopur', 'Dausa', 'Todabhim',
        'Sapotra', 'Karauli', 'Sawai Madhopur', 'Dausa', 'Todabhim',
        'Station Road', 'MG Road', 'Ring Road', 'Karauli Road', 'Sawai Madhopur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Todabhim': [
        'Todabhim City', 'Karauli', 'Sawai Madhopur', 'Hindaun', 'Dausa',
        'Sapotra', 'Karauli', 'Sawai Madhopur', 'Hindaun', 'Dausa',
        'Station Road', 'MG Road', 'Ring Road', 'Karauli Road', 'Sawai Madhopur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sapotra': [
        'Sapotra City', 'Karauli', 'Sawai Madhopur', 'Hindaun', 'Todabhim',
        'Dausa', 'Karauli', 'Sawai Madhopur', 'Hindaun', 'Todabhim',
        'Station Road', 'MG Road', 'Ring Road', 'Karauli Road', 'Sawai Madhopur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Deeg': [
        'Deeg City', 'Bharatpur', 'Bayana', 'Kaman', 'Nadbai',
        'Kumher', 'Weir', 'Bharatpur', 'Bayana', 'Kaman',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Bayana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bayana': [
        'Bayana City', 'Bharatpur', 'Deeg', 'Kaman', 'Nadbai',
        'Kumher', 'Weir', 'Bharatpur', 'Deeg', 'Kaman',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Deeg Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kaman': [
        'Kaman City', 'Bharatpur', 'Deeg', 'Bayana', 'Nadbai',
        'Kumher', 'Weir', 'Bharatpur', 'Deeg', 'Bayana',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Deeg Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nadbai': [
        'Nadbai City', 'Bharatpur', 'Deeg', 'Bayana', 'Kaman',
        'Kumher', 'Weir', 'Bharatpur', 'Deeg', 'Bayana',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Deeg Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kumher': [
        'Kumher City', 'Bharatpur', 'Deeg', 'Bayana', 'Kaman',
        'Nadbai', 'Weir', 'Bharatpur', 'Deeg', 'Bayana',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Deeg Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Weir': [
        'Weir City', 'Bharatpur', 'Deeg', 'Bayana', 'Kaman',
        'Nadbai', 'Kumher', 'Bharatpur', 'Deeg', 'Bayana',
        'Station Road', 'MG Road', 'Ring Road', 'Bharatpur Road', 'Deeg Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Fatehpur': [
        'Fatehpur City', 'Sikar', 'Lachhmangarh', 'Danta Ramgarh', 'Neem Ka Thana',
        'Sri Madhopur', 'Sikar', 'Lachhmangarh', 'Danta Ramgarh', 'Neem Ka Thana',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Lachhmangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Lachhmangarh': [
        'Lachhmangarh City', 'Sikar', 'Fatehpur', 'Danta Ramgarh', 'Neem Ka Thana',
        'Sri Madhopur', 'Sikar', 'Fatehpur', 'Danta Ramgarh', 'Neem Ka Thana',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Fatehpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Danta Ramgarh': [
        'Danta Ramgarh City', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Neem Ka Thana',
        'Sri Madhopur', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Neem Ka Thana',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Fatehpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Neem Ka Thana': [
        'Neem Ka Thana City', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh',
        'Sri Madhopur', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Fatehpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sri Madhopur': [
        'Sri Madhopur City', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh',
        'Neem Ka Thana', 'Sikar', 'Fatehpur', 'Lachhmangarh', 'Danta Ramgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Sikar Road', 'Fatehpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Deoli': [
        'Deoli City', 'Tonk', 'Jaipur', 'Uniara', 'Malpura',
        'Niwai', 'Tonk', 'Jaipur', 'Uniara', 'Malpura',
        'Station Road', 'MG Road', 'Ring Road', 'Tonk Road', 'Jaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Uniara': [
        'Uniara City', 'Tonk', 'Deoli', 'Jaipur', 'Malpura',
        'Niwai', 'Tonk', 'Deoli', 'Jaipur', 'Malpura',
        'Station Road', 'MG Road', 'Ring Road', 'Tonk Road', 'Deoli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Malpura': [
        'Malpura City', 'Tonk', 'Deoli', 'Uniara', 'Jaipur',
        'Niwai', 'Tonk', 'Deoli', 'Uniara', 'Jaipur',
        'Station Road', 'MG Road', 'Ring Road', 'Tonk Road', 'Deoli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Niwai': [
        'Niwai City', 'Tonk', 'Deoli', 'Uniara', 'Malpura',
        'Jaipur', 'Tonk', 'Deoli', 'Uniara', 'Malpura',
        'Station Road', 'MG Road', 'Ring Road', 'Tonk Road', 'Deoli Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Asind': [
        'Asind City', 'Bhilwara', 'Mandal', 'Shahpura', 'Raipur',
        'Gulabpura', 'Mandalgarh', 'Bhilwara', 'Mandal', 'Shahpura',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Mandal Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mandal': [
        'Mandal City', 'Bhilwara', 'Asind', 'Shahpura', 'Raipur',
        'Gulabpura', 'Mandalgarh', 'Bhilwara', 'Asind', 'Shahpura',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Asind Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Shahpura': [
        'Shahpura City', 'Bhilwara', 'Asind', 'Mandal', 'Raipur',
        'Gulabpura', 'Mandalgarh', 'Bhilwara', 'Asind', 'Mandal',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Asind Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Raipur': [
        'Raipur City', 'Bhilwara', 'Asind', 'Mandal', 'Shahpura',
        'Gulabpura', 'Mandalgarh', 'Bhilwara', 'Asind', 'Mandal',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Asind Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gulabpura': [
        'Gulabpura City', 'Bhilwara', 'Asind', 'Mandal', 'Shahpura',
        'Raipur', 'Mandalgarh', 'Bhilwara', 'Asind', 'Mandal',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Asind Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mandalgarh': [
        'Mandalgarh City', 'Bhilwara', 'Asind', 'Mandal', 'Shahpura',
        'Raipur', 'Gulabpura', 'Bhilwara', 'Asind', 'Mandal',
        'Station Road', 'MG Road', 'Ring Road', 'Bhilwara Road', 'Asind Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Begun': [
        'Begun City', 'Chittorgarh', 'Bhilwara', 'Pratapgarh', 'Banswara',
        'Nimbahera', 'Chittorgarh', 'Bhilwara', 'Pratapgarh', 'Banswara',
        'Station Road', 'MG Road', 'Ring Road', 'Chittorgarh Road', 'Bhilwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nimbahera': [
        'Nimbahera City', 'Chittorgarh', 'Bhilwara', 'Pratapgarh', 'Banswara',
        'Begun', 'Chittorgarh', 'Bhilwara', 'Pratapgarh', 'Banswara',
        'Station Road', 'MG Road', 'Ring Road', 'Chittorgarh Road', 'Bhilwara Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ghatol': [
        'Ghatol City', 'Banswara', 'Dungarpur', 'Pratapgarh', 'Chittorgarh',
        'Kushalgarh', 'Banswara', 'Dungarpur', 'Pratapgarh', 'Chittorgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Banswara Road', 'Dungarpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kushalgarh': [
        'Kushalgarh City', 'Banswara', 'Dungarpur', 'Pratapgarh', 'Chittorgarh',
        'Ghatol', 'Banswara', 'Dungarpur', 'Pratapgarh', 'Chittorgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Banswara Road', 'Dungarpur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ramganj Mandi': [
        'Ramganj Mandi City', 'Kota', 'Baran', 'Jhalawar', 'Bundi',
        'Sangod', 'Kota', 'Baran', 'Jhalawar', 'Bundi',
        'Station Road', 'MG Road', 'Ring Road', 'Kota Road', 'Baran Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sangod': [
        'Sangod City', 'Kota', 'Baran', 'Jhalawar', 'Bundi',
        'Ramganj Mandi', 'Kota', 'Baran', 'Jhalawar', 'Bundi',
        'Station Road', 'MG Road', 'Ring Road', 'Kota Road', 'Baran Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Salumbar': [
        'Salumbar City', 'Udaipur', 'Rajsamand', 'Nathdwara', 'Gogunda',
        'Kumbhalgarh', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road', 'Rajsamand Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gogunda': [
        'Gogunda City', 'Udaipur', 'Rajsamand', 'Nathdwara', 'Salumbar',
        'Kumbhalgarh', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road', 'Rajsamand Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kumbhalgarh': [
        'Kumbhalgarh City', 'Udaipur', 'Rajsamand', 'Nathdwara', 'Salumbar',
        'Gogunda', 'Jhadol', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jhadol': [
        'Jhadol City', 'Udaipur', 'Rajsamand', 'Nathdwara', 'Salumbar',
        'Gogunda', 'Kumbhalgarh', 'Rishabhdev', 'Udaipur', 'Rajsamand',
        'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road', 'Rajsamand Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rishabhdev': [
        'Rishabhdev City', 'Udaipur', 'Rajsamand', 'Nathdwara', 'Salumbar',
        'Gogunda', 'Kumbhalgarh', 'Jhadol', 'Udaipur', 'Rajsamand',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Udaipur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nasirabad': [
        'Nasirabad City', 'Ajmer', 'Kishangarh', 'Beawar', 'Kekri',
        'Sarwar', 'Ajmer', 'Kishangarh', 'Beawar', 'Kekri',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Kishangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kekri': [
        'Kekri City', 'Ajmer', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Sarwar', 'Ajmer', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Kishangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sarwar': [
        'Sarwar City', 'Ajmer', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Kekri', 'Ajmer', 'Kishangarh', 'Beawar', 'Nasirabad',
        'Station Road', 'MG Road', 'Ring Road', 'Ajmer Road', 'Kishangarh Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pindwara': [
        'Pindwara City', 'Sirohi', 'Mount Abu', 'Abu Road', 'Reodar',
        'Sheoganj', 'Sirohi', 'Mount Abu', 'Abu Road', 'Reodar',
        'Station Road', 'MG Road', 'Ring Road', 'Sirohi Road', 'Mount Abu Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Reodar': [
        'Reodar City', 'Sirohi', 'Mount Abu', 'Abu Road', 'Pindwara',
        'Sheoganj', 'Sirohi', 'Mount Abu', 'Abu Road', 'Pindwara',
        'Station Road', 'MG Road', 'Ring Road', 'Sirohi Road', 'Mount Abu Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sheoganj': [
        'Sheoganj City', 'Sirohi', 'Mount Abu', 'Abu Road', 'Pindwara',
        'Reodar', 'Sirohi', 'Mount Abu', 'Abu Road', 'Pindwara',
        'Station Road', 'MG Road', 'Ring Road', 'Sirohi Road', 'Mount Abu Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sanchore': [
        'Sanchore City', 'Jalore', 'Sirohi', 'Barmer', 'Jodhpur',
        'Bhinmal', 'Ahore', 'Jalore', 'Sirohi', 'Barmer',
        'Station Road', 'MG Road', 'Ring Road', 'Jalore Road', 'Sirohi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhinmal': [
        'Bhinmal City', 'Jalore', 'Sirohi', 'Sanchore', 'Barmer',
        'Ahore', 'Jalore', 'Sirohi', 'Sanchore', 'Barmer',
        'Station Road', 'MG Road', 'Ring Road', 'Jalore Road', 'Sirohi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ahore': [
        'Ahore City', 'Jalore', 'Sirohi', 'Sanchore', 'Bhinmal',
        'Barmer', 'Jalore', 'Sirohi', 'Sanchore', 'Bhinmal',
        'Station Road', 'MG Road', 'Ring Road', 'Jalore Road', 'Sirohi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pachpadra': [
        'Pachpadra City', 'Barmer', 'Balotra', 'Jaisalmer', 'Siwana',
        'Gudamalani', 'Barmer', 'Balotra', 'Jaisalmer', 'Siwana',
        'Station Road', 'MG Road', 'Ring Road', 'Barmer Road', 'Balotra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gudamalani': [
        'Gudamalani City', 'Barmer', 'Balotra', 'Jaisalmer', 'Siwana',
        'Pachpadra', 'Barmer', 'Balotra', 'Jaisalmer', 'Siwana',
        'Station Road', 'MG Road', 'Ring Road', 'Barmer Road', 'Balotra Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sam': [
        'Sam City', 'Jaisalmer', 'Barmer', 'Pokaran', 'Khuri',
        'Lodhruva', 'Amar Sagar', 'Jaisalmer', 'Barmer', 'Pokaran',
        'Desert Area', 'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Khuri': [
        'Khuri City', 'Jaisalmer', 'Barmer', 'Pokaran', 'Sam',
        'Lodhruva', 'Amar Sagar', 'Jaisalmer', 'Barmer', 'Pokaran',
        'Desert Area', 'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Lodhruva': [
        'Lodhruva City', 'Jaisalmer', 'Barmer', 'Pokaran', 'Sam',
        'Khuri', 'Amar Sagar', 'Jaisalmer', 'Barmer', 'Pokaran',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Amar Sagar': [
        'Amar Sagar City', 'Jaisalmer', 'Barmer', 'Pokaran', 'Sam',
        'Khuri', 'Lodhruva', 'Jaisalmer', 'Barmer', 'Pokaran',
        'Station Road', 'MG Road', 'Ring Road', 'Jaisalmer Road', 'Barmer Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Thanagazi': [
        'Thanagazi City', 'Alwar', 'Bhiwadi', 'Behror', 'Tijara',
        'Kishangarh', 'Rajgarh', 'Laxmangarh', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Bhiwadi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tijara': [
        'Tijara City', 'Alwar', 'Bhiwadi', 'Behror', 'Thanagazi',
        'Kishangarh', 'Rajgarh', 'Laxmangarh', 'Alwar', 'Bhiwadi',
        'Station Road', 'MG Road', 'Ring Road', 'Alwar Road', 'Bhiwadi Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Falna': [
        'Falna City', 'Pali', 'Sojat', 'Jaitaran', 'Jodhpur',
        'Raipur', 'Marwar Junction', 'Pali', 'Sojat', 'Jaitaran',
        'Station Road', 'MG Road', 'Ring Road', 'Pali Road', 'Sojat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Marwar Junction': [
        'Marwar Junction City', 'Pali', 'Sojat', 'Jaitaran', 'Falna',
        'Jodhpur', 'Raipur', 'Pali', 'Sojat', 'Jaitaran',
        'Station Road', 'MG Road', 'Ring Road', 'Pali Road', 'Sojat Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhopalgarh': [
        'Bhopalgarh City', 'Jodhpur', 'Osian', 'Bilara', 'Phalodi',
        'Shergarh', 'Jodhpur', 'Osian', 'Bilara', 'Phalodi',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Osian Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Shergarh': [
        'Shergarh City', 'Jodhpur', 'Osian', 'Bilara', 'Bhopalgarh',
        'Phalodi', 'Jodhpur', 'Osian', 'Bilara', 'Bhopalgarh',
        'Station Road', 'MG Road', 'Ring Road', 'Jodhpur Road', 'Osian Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Parbatsar': [
        'Parbatsar City', 'Nagaur', 'Makrana', 'Didwana', 'Merta',
        'Jodhpur', 'Ajmer', 'Nagaur', 'Makrana', 'Didwana',
        'Station Road', 'MG Road', 'Ring Road', 'Nagaur Road', 'Makrana Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    
    # Andhra Pradesh
    'Visakhapatnam': [
        'Dwaraka Nagar', 'MVP Colony', 'Seethammadhara', 'Madhurawada', 'Gajuwaka',
        'Maddilapalem', 'Akkayyapalem', 'Lawson Bay Colony', 'Beach Road', 'Rushikonda',
        'Waltair', 'Dabagardens', 'Siripuram', 'Asilmetta', 'Dondaparthy',
        'Maharanipeta', 'Pandurangapuram', 'Suryabagh', 'Lawsons Bay Colony', 'Yendada',
        'Pendurthi', 'Anakapalle', 'Bheemunipatnam', 'Vizianagaram', 'Srikakulam',
        'Station Road', 'MG Road', 'Ring Road', 'Beach Road', 'NH-5'
    ],
    'Vizag': [
        'Dwaraka Nagar', 'MVP Colony', 'Seethammadhara', 'Madhurawada', 'Gajuwaka',
        'Maddilapalem', 'Akkayyapalem', 'Lawson Bay Colony', 'Beach Road', 'Rushikonda',
        'Waltair', 'Dabagardens', 'Siripuram', 'Asilmetta', 'Dondaparthy',
        'Maharanipeta', 'Pandurangapuram', 'Suryabagh', 'Lawsons Bay Colony', 'Yendada',
        'Pendurthi', 'Anakapalle', 'Bheemunipatnam', 'Vizianagaram', 'Srikakulam',
        'Station Road', 'MG Road', 'Ring Road', 'Beach Road', 'NH-5'
    ],
    'Vijayawada': [
        'Benz Circle', 'MG Road', 'Eluru Road', 'Gunadala', 'Patamata',
        'Nidamanuru', 'Poranki', 'Kanuru', 'Bhavanipuram', 'Auto Nagar',
        'Siddhartha Nagar', 'Vijayawada City', 'One Town', 'Two Town', 'Three Town',
        'Labbipet', 'Governorpet', 'Benz Circle', 'Bhavanipuram', 'Auto Nagar',
        'Gunadala', 'Patamata', 'Nidamanuru', 'Poranki', 'Kanuru',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Guntur Road'
    ],
    'Guntur': [
        'Guntur City', 'Amaravati', 'Mangalagiri', 'Tadepalli', 'Tenali',
        'Narasaraopet', 'Chilakaluripet', 'Ponnur', 'Bapatla', 'Repalle',
        'Station Road', 'MG Road', 'Ring Road', 'Vijayawada Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nellore': [
        'Nellore City', 'Kavali', 'Gudur', 'Kovur', 'Atmakur',
        'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Chennai Road', 'Ongole Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kurnool': [
        'Kurnool City', 'Nandyal', 'Adoni', 'Yemmiganur', 'Dhone',
        'Nandikotkur', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Hyderabad Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rajahmundry': [
        'Rajahmundry City', 'Kakinada', 'Amalapuram', 'Ravulapalem', 'Mandapeta',
        'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Vijayawada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tirupati': [
        'Tirupati City', 'Tirumala', 'Chandragiri', 'Renigunta', 'Srikalahasti',
        'Puttur', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Tirumala',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Chittoor Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kakinada': [
        'Kakinada City', 'Rajahmundry', 'Amalapuram', 'Ravulapalem', 'Mandapeta',
        'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Port Area', 'Station Road', 'MG Road', 'Ring Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kadapa': [
        'Kadapa City', 'Proddatur', 'Jammalamadugu', 'Rayachoti', 'Rajampet',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Cuddapah': [
        'Kadapa City', 'Proddatur', 'Jammalamadugu', 'Rayachoti', 'Rajampet',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Anantapur': [
        'Anantapur City', 'Hindupur', 'Dharmavaram', 'Guntakal', 'Tadipatri',
        'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Bangalore Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chittoor': [
        'Chittoor City', 'Tirupati', 'Puttur', 'Chandragiri', 'Renigunta',
        'Srikalahasti', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Puttur',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Eluru': [
        'Eluru City', 'Vijayawada', 'Gudivada', 'Bhimavaram', 'Tadepalligudem',
        'Nuzvid', 'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu',
        'Station Road', 'MG Road', 'Ring Road', 'Vijayawada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ongole': [
        'Ongole City', 'Chirala', 'Bapatla', 'Addanki', 'Martur',
        'Darsi', 'Podili', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Guntur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Machilipatnam': [
        'Machilipatnam City', 'Gudivada', 'Bhimavaram', 'Tadepalligudem', 'Nuzvid',
        'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu', 'Eluru',
        'Port Area', 'Station Road', 'MG Road', 'Ring Road', 'Vijayawada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bhimavaram': [
        'Bhimavaram City', 'Eluru', 'Gudivada', 'Tadepalligudem', 'Nuzvid',
        'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tadepalligudem': [
        'Tadepalligudem City', 'Eluru', 'Bhimavaram', 'Gudivada', 'Nuzvid',
        'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Bhimavaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gudivada': [
        'Gudivada City', 'Vijayawada', 'Eluru', 'Bhimavaram', 'Tadepalligudem',
        'Nuzvid', 'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu',
        'Station Road', 'MG Road', 'Ring Road', 'Vijayawada Road', 'Eluru Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nuzvid': [
        'Nuzvid City', 'Vijayawada', 'Eluru', 'Gudivada', 'Bhimavaram',
        'Tadepalligudem', 'Jangareddygudem', 'Kovvur', 'Tanuku', 'Palakollu',
        'Station Road', 'MG Road', 'Ring Road', 'Vijayawada Road', 'Eluru Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tenali': [
        'Tenali City', 'Guntur', 'Vijayawada', 'Amaravati', 'Mangalagiri',
        'Tadepalli', 'Ponnur', 'Bapatla', 'Repalle', 'Chilakaluripet',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Vijayawada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Narasaraopet': [
        'Narasaraopet City', 'Guntur', 'Chilakaluripet', 'Ponnur', 'Bapatla',
        'Repalle', 'Tenali', 'Amaravati', 'Mangalagiri', 'Tadepalli',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chilakaluripet': [
        'Chilakaluripet City', 'Guntur', 'Narasaraopet', 'Ponnur', 'Bapatla',
        'Repalle', 'Tenali', 'Amaravati', 'Mangalagiri', 'Tadepalli',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Narasaraopet Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ponnur': [
        'Ponnur City', 'Guntur', 'Tenali', 'Bapatla', 'Repalle',
        'Amaravati', 'Mangalagiri', 'Tadepalli', 'Chilakaluripet', 'Narasaraopet',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Tenali Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bapatla': [
        'Bapatla City', 'Guntur', 'Ongole', 'Chirala', 'Tenali',
        'Ponnur', 'Repalle', 'Amaravati', 'Mangalagiri', 'Tadepalli',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Ongole Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Repalle': [
        'Repalle City', 'Guntur', 'Bapatla', 'Tenali', 'Ponnur',
        'Amaravati', 'Mangalagiri', 'Tadepalli', 'Chilakaluripet', 'Narasaraopet',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Bapatla Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Amaravati': [
        'Amaravati City', 'Guntur', 'Vijayawada', 'Mangalagiri', 'Tadepalli',
        'Tenali', 'Ponnur', 'Bapatla', 'Repalle', 'Chilakaluripet',
        'Capital Region', 'Station Road', 'MG Road', 'Ring Road', 'Guntur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mangalagiri': [
        'Mangalagiri City', 'Guntur', 'Amaravati', 'Vijayawada', 'Tadepalli',
        'Tenali', 'Ponnur', 'Bapatla', 'Repalle', 'Chilakaluripet',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Guntur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tadepalli': [
        'Tadepalli City', 'Guntur', 'Amaravati', 'Mangalagiri', 'Vijayawada',
        'Tenali', 'Ponnur', 'Bapatla', 'Repalle', 'Chilakaluripet',
        'Station Road', 'MG Road', 'Ring Road', 'Guntur Road', 'Amaravati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kavali': [
        'Kavali City', 'Nellore', 'Gudur', 'Kovur', 'Atmakur',
        'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gudur': [
        'Gudur City', 'Nellore', 'Kavali', 'Kovur', 'Atmakur',
        'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kovur': [
        'Kovur City', 'Nellore', 'Kavali', 'Gudur', 'Atmakur',
        'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Atmakur': [
        'Atmakur City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Udayagiri': [
        'Udayagiri City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Atmakur', 'Rapur', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rapur': [
        'Rapur City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Atmakur', 'Udayagiri', 'Venkatagiri', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Venkatagiri': [
        'Venkatagiri City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Atmakur', 'Udayagiri', 'Rapur', 'Sullurpeta', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Sullurpeta': [
        'Sullurpeta City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Atmakur', 'Udayagiri', 'Rapur', 'Venkatagiri', 'Tada',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tada': [
        'Tada City', 'Nellore', 'Kavali', 'Gudur', 'Kovur',
        'Atmakur', 'Udayagiri', 'Rapur', 'Venkatagiri', 'Sullurpeta',
        'Station Road', 'MG Road', 'Ring Road', 'Nellore Road', 'Chennai Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nandyal': [
        'Nandyal City', 'Kurnool', 'Adoni', 'Yemmiganur', 'Dhone',
        'Nandikotkur', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Adoni': [
        'Adoni City', 'Kurnool', 'Nandyal', 'Yemmiganur', 'Dhone',
        'Nandikotkur', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Yemmiganur': [
        'Yemmiganur City', 'Kurnool', 'Nandyal', 'Adoni', 'Dhone',
        'Nandikotkur', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dhone': [
        'Dhone City', 'Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur',
        'Nandikotkur', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Nandikotkur': [
        'Nandikotkur City', 'Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur',
        'Dhone', 'Kodumur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kodumur': [
        'Kodumur City', 'Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur',
        'Dhone', 'Nandikotkur', 'Pattikonda', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pattikonda': [
        'Pattikonda City', 'Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur',
        'Dhone', 'Nandikotkur', 'Kodumur', 'Alur', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Alur': [
        'Alur City', 'Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur',
        'Dhone', 'Nandikotkur', 'Kodumur', 'Pattikonda', 'Atmakur',
        'Station Road', 'MG Road', 'Ring Road', 'Kurnool Road', 'Hyderabad Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Proddatur': [
        'Proddatur City', 'Kadapa', 'Jammalamadugu', 'Rayachoti', 'Rajampet',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jammalamadugu': [
        'Jammalamadugu City', 'Kadapa', 'Proddatur', 'Rayachoti', 'Rajampet',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Proddatur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rayachoti': [
        'Rayachoti City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rajampet',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rajampet': [
        'Rajampet City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pulivendula': [
        'Pulivendula City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Rajampet', 'Mydukur', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mydukur': [
        'Mydukur City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Rajampet', 'Pulivendula', 'Kamalapuram', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kamalapuram': [
        'Kamalapuram City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Rajampet', 'Pulivendula', 'Mydukur', 'Badvel', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Badvel': [
        'Badvel City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Rajampet', 'Pulivendula', 'Mydukur', 'Kamalapuram', 'Siddhavatam',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Siddhavatam': [
        'Siddhavatam City', 'Kadapa', 'Proddatur', 'Jammalamadugu', 'Rayachoti',
        'Rajampet', 'Pulivendula', 'Mydukur', 'Kamalapuram', 'Badvel',
        'Station Road', 'MG Road', 'Ring Road', 'Kadapa Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Hindupur': [
        'Hindupur City', 'Anantapur', 'Dharmavaram', 'Guntakal', 'Tadipatri',
        'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Dharmavaram': [
        'Dharmavaram City', 'Anantapur', 'Hindupur', 'Guntakal', 'Tadipatri',
        'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Guntakal': [
        'Guntakal City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Tadipatri',
        'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tadipatri': [
        'Tadipatri City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Kurnool Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kalyandurg': [
        'Kalyandurg City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Tadipatri', 'Penukonda', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Penukonda': [
        'Penukonda City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Tadipatri', 'Kalyandurg', 'Kadiri', 'Madakasira', 'Rayadurg',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kadiri': [
        'Kadiri City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Tadipatri', 'Kalyandurg', 'Penukonda', 'Madakasira', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Madakasira': [
        'Madakasira City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Tadipatri', 'Kalyandurg', 'Penukonda', 'Kadiri', 'Rayadurg',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Rayadurg': [
        'Rayadurg City', 'Anantapur', 'Hindupur', 'Dharmavaram', 'Guntakal',
        'Tadipatri', 'Kalyandurg', 'Penukonda', 'Kadiri', 'Madakasira',
        'Station Road', 'MG Road', 'Ring Road', 'Anantapur Road', 'Bangalore Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Puttur': [
        'Puttur City', 'Tirupati', 'Chittoor', 'Chandragiri', 'Renigunta',
        'Srikalahasti', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Chittoor',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Chittoor Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chandragiri': [
        'Chandragiri City', 'Tirupati', 'Chittoor', 'Puttur', 'Renigunta',
        'Srikalahasti', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Chittoor',
        'Fort Area', 'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Renigunta': [
        'Renigunta City', 'Tirupati', 'Chittoor', 'Puttur', 'Chandragiri',
        'Srikalahasti', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Chittoor',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Chittoor Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Srikalahasti': [
        'Srikalahasti City', 'Tirupati', 'Chittoor', 'Puttur', 'Chandragiri',
        'Renigunta', 'Vadamalapeta', 'Karvetinagaram', 'Tirupati', 'Chittoor',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Vadamalapeta': [
        'Vadamalapeta City', 'Tirupati', 'Chittoor', 'Puttur', 'Chandragiri',
        'Renigunta', 'Srikalahasti', 'Karvetinagaram', 'Tirupati', 'Chittoor',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Chittoor Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Karvetinagaram': [
        'Karvetinagaram City', 'Tirupati', 'Chittoor', 'Puttur', 'Chandragiri',
        'Renigunta', 'Srikalahasti', 'Vadamalapeta', 'Tirupati', 'Chittoor',
        'Station Road', 'MG Road', 'Ring Road', 'Tirupati Road', 'Chittoor Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Amalapuram': [
        'Amalapuram City', 'Rajahmundry', 'Kakinada', 'Ravulapalem', 'Mandapeta',
        'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Rajahmundry Road', 'Kakinada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ravulapalem': [
        'Ravulapalem City', 'Rajahmundry', 'Kakinada', 'Amalapuram', 'Mandapeta',
        'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Rajahmundry Road', 'Kakinada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Mandapeta': [
        'Mandapeta City', 'Rajahmundry', 'Kakinada', 'Amalapuram', 'Ravulapalem',
        'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Rajahmundry Road', 'Kakinada Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tuni': [
        'Tuni City', 'Kakinada', 'Rajahmundry', 'Amalapuram', 'Ravulapalem',
        'Mandapeta', 'Peddapuram', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Peddapuram': [
        'Peddapuram City', 'Kakinada', 'Rajahmundry', 'Amalapuram', 'Ravulapalem',
        'Mandapeta', 'Tuni', 'Samalkot', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Samalkot': [
        'Samalkot City', 'Kakinada', 'Rajahmundry', 'Amalapuram', 'Ravulapalem',
        'Mandapeta', 'Tuni', 'Peddapuram', 'Ramachandrapuram', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Ramachandrapuram': [
        'Ramachandrapuram City', 'Kakinada', 'Rajahmundry', 'Amalapuram', 'Ravulapalem',
        'Mandapeta', 'Tuni', 'Peddapuram', 'Samalkot', 'Yanam',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Yanam': [
        'Yanam City', 'Kakinada', 'Rajahmundry', 'Amalapuram', 'Ravulapalem',
        'Mandapeta', 'Tuni', 'Peddapuram', 'Samalkot', 'Ramachandrapuram',
        'Station Road', 'MG Road', 'Ring Road', 'Kakinada Road', 'Rajahmundry Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Vizianagaram': [
        'Vizianagaram City', 'Visakhapatnam', 'Srikakulam', 'Parvathipuram', 'Bobbili',
        'Salur', 'Gajapathinagaram', 'Cheepurupalli', 'Vizianagaram', 'Visakhapatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Visakhapatnam Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Srikakulam': [
        'Srikakulam City', 'Vizianagaram', 'Visakhapatnam', 'Parvathipuram', 'Bobbili',
        'Salur', 'Gajapathinagaram', 'Cheepurupalli', 'Vizianagaram', 'Visakhapatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Visakhapatnam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Parvathipuram': [
        'Parvathipuram City', 'Vizianagaram', 'Srikakulam', 'Bobbili', 'Salur',
        'Gajapathinagaram', 'Cheepurupalli', 'Vizianagaram', 'Srikakulam', 'Bobbili',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bobbili': [
        'Bobbili City', 'Vizianagaram', 'Srikakulam', 'Parvathipuram', 'Salur',
        'Gajapathinagaram', 'Cheepurupalli', 'Vizianagaram', 'Srikakulam', 'Parvathipuram',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Salur': [
        'Salur City', 'Vizianagaram', 'Srikakulam', 'Parvathipuram', 'Bobbili',
        'Gajapathinagaram', 'Cheepurupalli', 'Vizianagaram', 'Srikakulam', 'Parvathipuram',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Gajapathinagaram': [
        'Gajapathinagaram City', 'Vizianagaram', 'Srikakulam', 'Parvathipuram', 'Bobbili',
        'Salur', 'Cheepurupalli', 'Vizianagaram', 'Srikakulam', 'Parvathipuram',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Cheepurupalli': [
        'Cheepurupalli City', 'Vizianagaram', 'Srikakulam', 'Parvathipuram', 'Bobbili',
        'Salur', 'Gajapathinagaram', 'Vizianagaram', 'Srikakulam', 'Parvathipuram',
        'Station Road', 'MG Road', 'Ring Road', 'Vizianagaram Road', 'Srikakulam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Anakapalle': [
        'Anakapalle City', 'Visakhapatnam', 'Vizianagaram', 'Srikakulam', 'Bheemunipatnam',
        'Pendurthi', 'Yendada', 'Visakhapatnam', 'Vizianagaram', 'Srikakulam',
        'Station Road', 'MG Road', 'Ring Road', 'Visakhapatnam Road', 'Vizianagaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Bheemunipatnam': [
        'Bheemunipatnam City', 'Visakhapatnam', 'Anakapalle', 'Vizianagaram', 'Srikakulam',
        'Pendurthi', 'Yendada', 'Visakhapatnam', 'Anakapalle', 'Vizianagaram',
        'Beach Area', 'Station Road', 'MG Road', 'Ring Road', 'Visakhapatnam Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Pendurthi': [
        'Pendurthi City', 'Visakhapatnam', 'Anakapalle', 'Bheemunipatnam', 'Vizianagaram',
        'Srikakulam', 'Yendada', 'Visakhapatnam', 'Anakapalle', 'Bheemunipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Visakhapatnam Road', 'Anakapalle Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Chirala': [
        'Chirala City', 'Ongole', 'Bapatla', 'Addanki', 'Martur',
        'Darsi', 'Podili', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Bapatla Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Addanki': [
        'Addanki City', 'Ongole', 'Chirala', 'Bapatla', 'Martur',
        'Darsi', 'Podili', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Martur': [
        'Martur City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Darsi', 'Podili', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Darsi': [
        'Darsi City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Martur', 'Podili', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Podili': [
        'Podili City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Martur', 'Darsi', 'Kanigiri', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kanigiri': [
        'Kanigiri City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Martur', 'Darsi', 'Podili', 'Markapur', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Markapur': [
        'Markapur City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Martur', 'Darsi', 'Podili', 'Kanigiri', 'Giddalur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Giddalur': [
        'Giddalur City', 'Ongole', 'Chirala', 'Bapatla', 'Addanki',
        'Martur', 'Darsi', 'Podili', 'Kanigiri', 'Markapur',
        'Station Road', 'MG Road', 'Ring Road', 'Ongole Road', 'Chirala Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Jangareddygudem': [
        'Jangareddygudem City', 'Eluru', 'Bhimavaram', 'Tadepalligudem', 'Gudivada',
        'Nuzvid', 'Kovvur', 'Tanuku', 'Palakollu', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Bhimavaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Kovvur': [
        'Kovvur City', 'Eluru', 'Bhimavaram', 'Tadepalligudem', 'Gudivada',
        'Nuzvid', 'Jangareddygudem', 'Tanuku', 'Palakollu', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Bhimavaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Tanuku': [
        'Tanuku City', 'Eluru', 'Bhimavaram', 'Tadepalligudem', 'Gudivada',
        'Nuzvid', 'Jangareddygudem', 'Kovvur', 'Palakollu', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Bhimavaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    'Palakollu': [
        'Palakollu City', 'Eluru', 'Bhimavaram', 'Tadepalligudem', 'Gudivada',
        'Nuzvid', 'Jangareddygudem', 'Kovvur', 'Tanuku', 'Machilipatnam',
        'Station Road', 'MG Road', 'Ring Road', 'Eluru Road', 'Bhimavaram Road',
        'Vidyanagar', 'Ashok Nagar', 'Shivaji Nagar', 'Gandhi Nagar', 'Model Town'
    ],
    
    # Kerala
    'Kochi': [
        'Marine Drive', 'Fort Kochi', 'Mattancherry', 'Ernakulam', 'Edapally',
        'Kakkanad', 'Infopark', 'Smart City', 'Vyttila', 'Palarivattom',
        'Kaloor', 'MG Road', 'Banerji Road', 'Chittoor Road', 'Panampilly Nagar',
        'Aluva', 'Kalamassery', 'Eloor', 'Perumbavoor', 'Angamaly',
        'Kochi City', 'Ernakulam', 'Fort Kochi', 'Mattancherry', 'Marine Drive',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Cochin': [
        'Marine Drive', 'Fort Kochi', 'Mattancherry', 'Ernakulam', 'Edapally',
        'Kakkanad', 'Infopark', 'Smart City', 'Vyttila', 'Palarivattom',
        'Kaloor', 'MG Road', 'Banerji Road', 'Chittoor Road', 'Panampilly Nagar',
        'Aluva', 'Kalamassery', 'Eloor', 'Perumbavoor', 'Angamaly',
        'Kochi City', 'Ernakulam', 'Fort Kochi', 'Mattancherry', 'Marine Drive',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Thiruvananthapuram': [
        'Thiruvananthapuram City', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam', 'Kesavadasapuram',
        'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Kulathoor', 'Vattiyoorkavu',
        'Karamana', 'Pettah', 'Chalai', 'Fort', 'Palayam',
        'Thampanoor', 'East Fort', 'West Fort', 'Museum', 'Nanthancode',
        'Kowdiar', 'Vellayambalam', 'Sasthamangalam', 'Kesavadasapuram', 'Pattom',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Trivandrum': [
        'Thiruvananthapuram City', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam', 'Kesavadasapuram',
        'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Kulathoor', 'Vattiyoorkavu',
        'Karamana', 'Pettah', 'Chalai', 'Fort', 'Palayam',
        'Thampanoor', 'East Fort', 'West Fort', 'Museum', 'Nanthancode',
        'Kowdiar', 'Vellayambalam', 'Sasthamangalam', 'Kesavadasapuram', 'Pattom',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Kozhikode': [
        'Kozhikode City', 'Calicut', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy',
        'Beypore', 'Elathur', 'Kallayi', 'Palayam', 'Mananchira',
        'Mavoor Road', 'Mavoor', 'Feroke', 'Ramanattukara', 'Kunnamangalam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Calicut': [
        'Kozhikode City', 'Calicut', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy',
        'Beypore', 'Elathur', 'Kallayi', 'Palayam', 'Mananchira',
        'Mavoor Road', 'Mavoor', 'Feroke', 'Ramanattukara', 'Kunnamangalam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Thrissur': [
        'Thrissur City', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Poonkunnam', 'Ayyanthole', 'Patturaikkal', 'Kuttanellur', 'Puzhakkal',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Trichur': [
        'Thrissur City', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Poonkunnam', 'Ayyanthole', 'Patturaikkal', 'Kuttanellur', 'Puzhakkal',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kollam': [
        'Kollam City', 'Quilon', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam',
        'Asramam', 'Kollam Beach', 'Port Area', 'Kollam City', 'Quilon',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Quilon': [
        'Kollam City', 'Quilon', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam',
        'Asramam', 'Kollam Beach', 'Port Area', 'Kollam City', 'Quilon',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kannur': [
        'Kannur City', 'Cannanore', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri',
        'Kannur City', 'Cannanore', 'Thalassery', 'Payyannur', 'Iritty',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Cannanore': [
        'Kannur City', 'Cannanore', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri',
        'Kannur City', 'Cannanore', 'Thalassery', 'Payyannur', 'Iritty',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Alappuzha': [
        'Alappuzha City', 'Alleppey', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Mavelikkara', 'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom',
        'Alappuzha City', 'Alleppey', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Alleppey': [
        'Alappuzha City', 'Alleppey', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Mavelikkara', 'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom',
        'Alappuzha City', 'Alleppey', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kottayam': [
        'Kottayam City', 'Changanassery', 'Pala', 'Vaikom', 'Ettumanoor',
        'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Erattupetta',
        'Kottayam City', 'Changanassery', 'Pala', 'Vaikom', 'Ettumanoor',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Palakkad': [
        'Palakkad City', 'Palghat', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur',
        'Palakkad City', 'Palghat', 'Ottapalam', 'Shoranur', 'Chittur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Palghat': [
        'Palakkad City', 'Palghat', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur',
        'Palakkad City', 'Palghat', 'Ottapalam', 'Shoranur', 'Chittur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Malappuram': [
        'Malappuram City', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram City', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Manjeri': [
        'Manjeri City', 'Malappuram', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Perinthalmanna': [
        'Perinthalmanna City', 'Malappuram', 'Manjeri', 'Tirur', 'Ponnani',
        'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Tirur': [
        'Tirur City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Ponnani',
        'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Ponnani': [
        'Ponnani City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Kondotty': [
        'Kondotty City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Ponnani', 'Kottakkal', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Kottakkal': [
        'Kottakkal City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Ponnani', 'Kondotty', 'Valanchery', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Valanchery': [
        'Valanchery City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Ponnani', 'Kondotty', 'Kottakkal', 'Tanur', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Tanur': [
        'Tanur City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Ponnani', 'Kondotty', 'Kottakkal', 'Valanchery', 'Parappanangadi',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Parappanangadi': [
        'Parappanangadi City', 'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur',
        'Ponnani', 'Kondotty', 'Kottakkal', 'Valanchery', 'Tanur',
        'Malappuram', 'Manjeri', 'Perinthalmanna', 'Tirur', 'Ponnani',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Guruvayur': [
        'Guruvayur City', 'Thrissur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Temple Area', 'Thrissur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kodungallur': [
        'Kodungallur City', 'Thrissur', 'Guruvayur', 'Irinjalakuda', 'Chalakudy',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Irinjalakuda': [
        'Irinjalakuda City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Chalakudy',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Chalakudy': [
        'Chalakudy City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kunnamkulam': [
        'Kunnamkulam City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Chalakudy', 'Wadakkanchery', 'Mala', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Wadakkanchery': [
        'Wadakkanchery City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Chalakudy', 'Kunnamkulam', 'Mala', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Mala': [
        'Mala City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Chalakudy', 'Kunnamkulam', 'Wadakkanchery', 'Kodakara', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kodakara': [
        'Kodakara City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Chalakudy', 'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Mukundapuram',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Mukundapuram': [
        'Mukundapuram City', 'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda',
        'Chalakudy', 'Kunnamkulam', 'Wadakkanchery', 'Mala', 'Kodakara',
        'Thrissur', 'Guruvayur', 'Kodungallur', 'Irinjalakuda', 'Chalakudy',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Paravur': [
        'Paravur City', 'Kollam', 'Karunagappally', 'Kottarakkara', 'Punalur',
        'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Karunagappally': [
        'Karunagappally City', 'Kollam', 'Paravur', 'Kottarakkara', 'Punalur',
        'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kottarakkara': [
        'Kottarakkara City', 'Kollam', 'Paravur', 'Karunagappally', 'Punalur',
        'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Punalur': [
        'Punalur City', 'Kollam', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Sasthamkotta', 'Chavara', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Sasthamkotta': [
        'Sasthamkotta City', 'Kollam', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Chavara', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Chavara': [
        'Chavara City', 'Kollam', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Sasthamkotta', 'Ochira', 'Chadayamangalam', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Ochira': [
        'Ochira City', 'Kollam', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Sasthamkotta', 'Chavara', 'Chadayamangalam', 'Kollam',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'NH-66'
    ],
    'Chadayamangalam': [
        'Chadayamangalam City', 'Kollam', 'Paravur', 'Karunagappally', 'Kottarakkara',
        'Punalur', 'Sasthamkotta', 'Chavara', 'Ochira', 'Kollam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Thalassery': [
        'Thalassery City', 'Kannur', 'Payyannur', 'Iritty', 'Taliparamba',
        'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Payyannur': [
        'Payyannur City', 'Kannur', 'Thalassery', 'Iritty', 'Taliparamba',
        'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Iritty': [
        'Iritty City', 'Kannur', 'Thalassery', 'Payyannur', 'Taliparamba',
        'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Taliparamba': [
        'Taliparamba City', 'Kannur', 'Thalassery', 'Payyannur', 'Iritty',
        'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Mattannur': [
        'Mattannur City', 'Kannur', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Kuthuparamba', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Kuthuparamba': [
        'Kuthuparamba City', 'Kannur', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Mattannur', 'Sreekandapuram', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Sreekandapuram': [
        'Sreekandapuram City', 'Kannur', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Mattannur', 'Kuthuparamba', 'Pappinisseri', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Pappinisseri': [
        'Pappinisseri City', 'Kannur', 'Thalassery', 'Payyannur', 'Iritty',
        'Taliparamba', 'Mattannur', 'Kuthuparamba', 'Sreekandapuram', 'Kannur',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Ambalapuzha': [
        'Ambalapuzha City', 'Alappuzha', 'Cherthala', 'Kayamkulam', 'Mavelikkara',
        'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'NH-66'
    ],
    'Cherthala': [
        'Cherthala City', 'Alappuzha', 'Ambalapuzha', 'Kayamkulam', 'Mavelikkara',
        'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kayamkulam': [
        'Kayamkulam City', 'Alappuzha', 'Ambalapuzha', 'Cherthala', 'Mavelikkara',
        'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Mavelikkara': [
        'Mavelikkara City', 'Alappuzha', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Chengannur', 'Haripad', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Chengannur': [
        'Chengannur City', 'Alappuzha', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Mavelikkara', 'Haripad', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Haripad': [
        'Haripad City', 'Alappuzha', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Mavelikkara', 'Chengannur', 'Kuttanad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kuttanad': [
        'Kuttanad City', 'Alappuzha', 'Ambalapuzha', 'Cherthala', 'Kayamkulam',
        'Mavelikkara', 'Chengannur', 'Haripad', 'Kumarakom', 'Alappuzha',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-47'
    ],
    'Kumarakom': [
        'Kumarakom City', 'Kottayam', 'Alappuzha', 'Changanassery', 'Pala',
        'Vaikom', 'Ettumanoor', 'Puthuppally', 'Kanjirappally', 'Kottayam',
        'Backwaters', 'Station Road', 'MG Road', 'Ring Road', 'NH-47'
    ],
    'Changanassery': [
        'Changanassery City', 'Kottayam', 'Pala', 'Vaikom', 'Ettumanoor',
        'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Pala': [
        'Pala City', 'Kottayam', 'Changanassery', 'Vaikom', 'Ettumanoor',
        'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Vaikom': [
        'Vaikom City', 'Kottayam', 'Changanassery', 'Pala', 'Ettumanoor',
        'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Kottayam',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'NH-47'
    ],
    'Ettumanoor': [
        'Ettumanoor City', 'Kottayam', 'Changanassery', 'Pala', 'Vaikom',
        'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Kottayam',
        'Temple Area', 'Station Road', 'MG Road', 'Ring Road', 'NH-47'
    ],
    'Puthuppally': [
        'Puthuppally City', 'Kottayam', 'Changanassery', 'Pala', 'Vaikom',
        'Ettumanoor', 'Kumarakom', 'Kanjirappally', 'Mundakayam', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Kanjirappally': [
        'Kanjirappally City', 'Kottayam', 'Changanassery', 'Pala', 'Vaikom',
        'Ettumanoor', 'Puthuppally', 'Kumarakom', 'Mundakayam', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Mundakayam': [
        'Mundakayam City', 'Kottayam', 'Changanassery', 'Pala', 'Vaikom',
        'Ettumanoor', 'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Erattupetta': [
        'Erattupetta City', 'Kottayam', 'Changanassery', 'Pala', 'Vaikom',
        'Ettumanoor', 'Puthuppally', 'Kumarakom', 'Kanjirappally', 'Kottayam',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Ottapalam': [
        'Ottapalam City', 'Palakkad', 'Shoranur', 'Chittur', 'Alathur',
        'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Shoranur': [
        'Shoranur City', 'Palakkad', 'Ottapalam', 'Chittur', 'Alathur',
        'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Chittur': [
        'Chittur City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Alathur',
        'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Alathur': [
        'Alathur City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Chittur',
        'Mannarkkad', 'Pattambi', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Mannarkkad': [
        'Mannarkkad City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Pattambi', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Pattambi': [
        'Pattambi City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Mannarkkad', 'Kollengode', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Kollengode': [
        'Kollengode City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Mannarkkad', 'Pattambi', 'Koduvayur', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Koduvayur': [
        'Koduvayur City', 'Palakkad', 'Ottapalam', 'Shoranur', 'Chittur',
        'Alathur', 'Mannarkkad', 'Pattambi', 'Kollengode', 'Palakkad',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Mavoor': [
        'Mavoor City', 'Kozhikode', 'Feroke', 'Ramanattukara', 'Kunnamangalam',
        'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Feroke': [
        'Feroke City', 'Kozhikode', 'Mavoor', 'Ramanattukara', 'Kunnamangalam',
        'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Ramanattukara': [
        'Ramanattukara City', 'Kozhikode', 'Mavoor', 'Feroke', 'Kunnamangalam',
        'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Kunnamangalam': [
        'Kunnamangalam City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Koduvally', 'Thamarassery', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Koduvally': [
        'Koduvally City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Thamarassery', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Thamarassery': [
        'Thamarassery City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Vadakara', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Vadakara': [
        'Vadakara City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Koyilandy', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Koyilandy': [
        'Koyilandy City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Beypore': [
        'Beypore City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Kozhikode',
        'Port Area', 'Station Road', 'MG Road', 'Ring Road', 'NH-66'
    ],
    'Elathur': [
        'Elathur City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Kallayi': [
        'Kallayi City', 'Kozhikode', 'Mavoor', 'Feroke', 'Ramanattukara',
        'Kunnamangalam', 'Koduvally', 'Thamarassery', 'Vadakara', 'Kozhikode',
        'Station Road', 'MG Road', 'Ring Road', 'NH-66', 'NH-17'
    ],
    'Aluva': [
        'Aluva City', 'Kochi', 'Kalamassery', 'Eloor', 'Perumbavoor',
        'Angamaly', 'Ernakulam', 'Edapally', 'Kakkanad', 'Kochi',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kalamassery': [
        'Kalamassery City', 'Kochi', 'Aluva', 'Eloor', 'Perumbavoor',
        'Angamaly', 'Ernakulam', 'Edapally', 'Kakkanad', 'Kochi',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Eloor': [
        'Eloor City', 'Kochi', 'Aluva', 'Kalamassery', 'Perumbavoor',
        'Angamaly', 'Ernakulam', 'Edapally', 'Kakkanad', 'Kochi',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Perumbavoor': [
        'Perumbavoor City', 'Kochi', 'Aluva', 'Kalamassery', 'Eloor',
        'Angamaly', 'Ernakulam', 'Edapally', 'Kakkanad', 'Kochi',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Angamaly': [
        'Angamaly City', 'Kochi', 'Aluva', 'Kalamassery', 'Eloor',
        'Perumbavoor', 'Ernakulam', 'Edapally', 'Kakkanad', 'Kochi',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-17'
    ],
    'Kazhakoottam': [
        'Kazhakoottam City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kaniyapuram', 'Kulathoor', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Kaniyapuram': [
        'Kaniyapuram City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kulathoor', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Kulathoor': [
        'Kulathoor City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Vattiyoorkavu': [
        'Vattiyoorkavu City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Karamana': [
        'Karamana City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Pettah': [
        'Pettah City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Chalai': [
        'Chalai City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Fort': [
        'Fort City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Palayam': [
        'Palayam City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Thampanoor': [
        'Thampanoor City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
    ],
    'Nanthancode': [
        'Nanthancode City', 'Thiruvananthapuram', 'Kowdiar', 'Vellayambalam', 'Sasthamangalam',
        'Kesavadasapuram', 'Pattom', 'Kazhakoottam', 'Kaniyapuram', 'Thiruvananthapuram',
        'Station Road', 'MG Road', 'Ring Road', 'NH-47', 'NH-66'
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
