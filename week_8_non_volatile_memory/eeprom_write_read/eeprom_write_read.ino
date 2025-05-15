char ReadByte(int address)
{
    char* data_register = (char*) 0x40;       //Points to EEDR
    volatile char *control_register = (char*) 0x3F; //Points to EECR
    int* address_register = (int*) 0x41;      //Points to EEAR. Note that int is 16bit on ATmega328p
                                               //This pointer points to both low byte and high byte
                                               //of EEAR

    while (((*control_register) & 2))         //If the data is being written (EEPE is high)
    {
        //do nothing
    }
    *address_register = address;               //Stores the address in the EEAR
    *control_register = 1;                     //Set EERE (Initiate reading)
    return *data_register;                     //Return the contents of the data register (EEDR)
}

void WriteByte(int address, char data)
{
    char* data_register = (char*) 0x40;       //Points to EEDR
    volatile char *control_register = (char*) 0x3F; //Points to EECR
    int* address_register = (int*) 0x41;      //Points to EEAR. Note that int is 16bit on ATmega328p
                                               //This pointer points to both low byte and high byte
                                               //of EEAR

    while (((*control_register) & 2))         //If the data is being written (EEPE is high)
    {
        //do nothing
    }
    *address_register = address;               //Stores the address in the EEAR
    *data_register = data;                     //Stores the data in the EEDR
    *control_register = 4;                     //Enable Master Write (Set EEMPE)
    *control_register |= 2;                    //Start writing (Set EEPE)
}

int main()
{
    Serial.begin(9600);

    WriteByte(115, 20);                       //Write a value of 168 to the memory location 115
    unsigned char a = ReadByte(115);           //Read the value at memory location 115
    Serial.println(a);                         //Prints the value

    return 0; // Assuming a typical C/C++ main return
}