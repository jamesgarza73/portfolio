/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pokergame;

/**
 *
 * @author HowleR
 */
public class Card 
{
    String[] suits   = {"Hearts","Diamonds","Spades","Clubs"};
    String[] values  = {"Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"};
    //  the following ints could be strings(will use the same process)
    int suit;
    int value;

    @Override
    public String toString() 
    {
        return ""+ values[value]+" of "+suits[suit];
    }
    
    
}






























