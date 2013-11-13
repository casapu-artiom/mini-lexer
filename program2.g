func main() {
	a, b, tmp Integer;
	read(a); read(b);
	while (b != 0)  {
		tmp = a % b;
		b = a;
		a = tmp;
	}
	write(a);
}
