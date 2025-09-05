using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List<string> todoList = new List<string>();
        while (true)
        {
            Console.WriteLine("\nTo-Do List:");
            for (int i = 0; i < todoList.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {todoList[i]}");
            }

            Console.WriteLine("\nOptions:");
            Console.WriteLine("1. Add item");
            Console.WriteLine("2. Remove item");
            Console.WriteLine("3. Exit");
            Console.Write("Choose an option: ");
            string input = Console.ReadLine();

            if (input == "1")
            {
                Console.Write("Enter new to-do item: ");
                string item = Console.ReadLine();
                if (!string.IsNullOrWhiteSpace(item))
                    todoList.Add(item);
            }
            else if (input == "2")
            {
                Console.Write("Enter item number to remove: ");
                if (int.TryParse(Console.ReadLine(), out int index) && index > 0 && index <= todoList.Count)
                    todoList.RemoveAt(index - 1);
            }
            else if (input == "3")
            {
                break;
            }
        }
    }
}