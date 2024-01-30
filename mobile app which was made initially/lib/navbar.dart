import 'package:flutter/material.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import './home.dart';
import './quiz.dart';

class Navbar extends StatefulWidget {
  const Navbar({super.key});

  @override
  State<Navbar> createState() => NavbarState();
}

class NavbarState extends State<Navbar> {
  int _selectedIndex = 0;
  static const List<Widget> _widgetOptions = <Widget>[
    Home(),
    quiz(),
    Text(
      'Profile'
    ),
  ];


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      // appBar: AppBar(
      //   elevation: 20,
      //   title: const Text('Sign Lang'),
      // ),
      body:
      _widgetOptions.elementAt(_selectedIndex),

      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              blurRadius: 20,
              color: Colors.black.withOpacity(.1),
            )
          ],
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 15.0, vertical: 8),
            child: GNav(
              rippleColor: Colors.grey[300]!,
              hoverColor: Colors.grey[100]!,
              gap: 8,
              activeColor: Colors.black,
              iconSize: 24,
              padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              duration: Duration(milliseconds: 400),
              tabBackgroundColor: Colors.grey[100]!,
              color: Colors.black,
              tabs: [
                GButton(
                  icon: Icons.enhance_photo_translate,
                  text: 'Live translation',
                ),
                GButton(
                  icon: Icons.quiz,
                  text: 'quiz',
                ),
                GButton(
                  icon: Icons.person,
                  text: 'Profile',
                ),
              ],
              selectedIndex: _selectedIndex,
              onTabChange: (index) {
                setState(() {
                  _selectedIndex = index;
                });
              },
            ),
          ),
        ),
      ),
    );
  }
}