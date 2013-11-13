func main() {
	n,i,s Integer; x Integer[100];
	read(n);
	i = 0;
	while (i < n) {
		read(x[i]);
		i = i + 1;
    }
	i = 0;
	s = 0;
	while (i < n) {
		s = s + x[i];
		i = i + 1;
}
write(s);
}
