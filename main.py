import sys
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from scanner_engine import CyberEngine
from banners import get_joke

console = Console()

def run_mega_audit(target):
    console.print(Panel.fit(f"[bold red]QBT-RECON PRO[/bold red]\n[white]{get_joke()}[/white]", border_style="red"))
    
    engine = CyberEngine(target)
    
    # Списки для хранения результатов
    found_subs = []
    found_ports = []
    found_files = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        
        # 1. ПОДДОМЕНЫ
        task1 = progress.add_task("[yellow]Разведка поддоменов...", total=None)
        found_subs = engine.check_subdomains()
        progress.update(task1, completed=True, description="[green]Поддомены собраны!")

        # 2. ПОРТЫ
        task2 = progress.add_task("[blue]Скан критических портов...", total=None)
        common_ports = [21, 22, 23, 80, 443, 3306, 5432, 8080]
        for p in common_ports:
            if engine.check_port(p):
                found_ports.append(str(p))
        progress.update(task2, completed=True, description="[green]Порты проверены!")

        # 3. ФАЙЛЫ
        task3 = progress.add_task("[red]Поиск 'забытых' файлов...", total=None)
        found_files = engine.brute_paths()
        progress.update(task3, completed=True, description="[green]Файлы прочесаны!")

    # --- ВОТ ТУТ МАГИЯ ВЫВОДА В ТЕРМИНАЛ ---
    summary = Table(title=f"\n[bold gold1]📊 ИТОГОВЫЙ ОТЧЕТ: {target}[/bold gold1]", show_header=True, header_style="bold magenta", expand=True)
    summary.add_column("КАТЕГОРИЯ", style="cyan", width=20)
    summary.add_column("РЕЗУЛЬТАТ", style="white")

    # Добавляем поддомены
    sub_text = ", ".join(found_subs) if found_subs else "[dim red]Ничего не найдено[/dim red]"
    summary.add_row("🌐 Поддомены", sub_text)

    # Добавляем порты
    port_text = ", ".join(found_ports) if found_ports else "[dim red]Все закрыто[/dim red]"
    summary.add_row("🔌 Открытые порты", port_text)

    # Добавляем файлы
    file_text = ", ".join(found_files) if found_files else "[dim green]Чисто (дырок не видно)[/dim green]"
    summary.add_row("📂 Файлы/Конфиги", file_text)

    console.print(summary)

    # Сохранение в файл (чтобы не потерять)
    filename = f"audit_{target.replace('.', '_')}.md"
    with open(filename, "w") as f:
        f.write(f"# Audit for {target}\nPorts: {found_ports}\nSubs: {found_subs}\nFiles: {found_files}")
    
    console.print(f"\n[bold cyan][i][/bold cyan] Подробный отчет сохранен в: [bold white]{filename}[/bold white]")

if __name__ == "__main__":
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    run_mega_audit(target_arg)
