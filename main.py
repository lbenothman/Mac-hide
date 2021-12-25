import typer
from InquirerPy import inquirer
import subprocess
import psutil


app = typer.Typer()


@app.command()
def get():
    """
    List the network interfaces and display the mac address
    """
    interface = select_network_interface()
    mac_address = get_mac_address(interface)          
    typer.echo(f"The mac address is {mac_address}")


@app.command()
def patch():
    """
    List the network interfaces and change the mac address
    """    
    interface = select_network_interface()
    change_mac_address(interface)
    mac_address = get_mac_address(interface)

    typer.echo(f"The new mac address is: {mac_address}")


def select_network_interface():
    """
    Allow the user to select a network interface

    Returns:
        string: network interface
    """    
    interfaces = psutil.net_if_addrs()

    if len(interfaces) == 0:
        typer.echo(f"There is no branch to checkout")
        return

    return inquirer.select(
        message="Select the interface:",
        choices=interfaces.keys(),
    ).execute()

   
def change_mac_address(interface):
    """
    Change the mac address

    Args:
        interface string: The network interface
    """    
    subprocess.call(["ifconfig", interface, "ether", "00:11:22:33:44:66"])
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac_address(interface):
    """
    Return the mac address

    Args:
        interface string: The network interface

    Returns:
        string: mac address
    """
    interfaces = psutil.net_if_addrs()
    snics = interfaces[interface]

    for snic in snics:
        if snic.family == psutil.AF_LINK:
            return snic.address  


if __name__ == "__main__":
    app()
